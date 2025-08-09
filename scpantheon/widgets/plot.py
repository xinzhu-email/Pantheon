from bokeh.plotting import figure, ColumnDataSource
from bokeh.models import LogColorMapper, ColorBar
from bokeh.palettes import d3
from bokeh.transform import linear_cmap
from scipy.sparse import issparse
from scpantheon.buttons import make_layout, make_widget, LayoutOrientation, Widget_type
from scpantheon.base import Base
from scpantheon.stdata import DataCat
from scpantheon.tabs import refresh
import colorcet as cc
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import numpy as np
import pandas as pd
import stdata as dt

color_list = d3['Category20c'][20]

class ScatterPlot:
    def __init__(
        self,
        is_continuous: bool,
        contrast_bar: bool | None,
        source: ColumnDataSource | None
    ):
        self.is_continuous = is_continuous
        self.plot = None
        self.glyphs = None
        if self.is_continuous == True:
            if contrast_bar is None:
                self.contrast_bar = False
            else:
                self.contrast_bar = contrast_bar
        else:
            if contrast_bar is not None:
                print("Warning: discrete scatter plot has no attribute contrast_bar")
            self.contrast_bar = None
        self.source = source
        self.plot_figure()
    
    def plot_figure(self):
        if self.is_continuous:
            width = 550
        else:
            width = 500
        if self.source:
            plot = figure(width = width, height = 500, tools = "pan,lasso_select,box_select,tap,wheel_zoom,save,hover")
            plot.xaxis.axis_label, plot.yaxis.axis_label = self.source.column_names[0], self.source.column_names[1]
            if self.is_continuous:
                if self.contrast_bar:
                    cmap = cm.get_cmap('jet', 256)
                    palette = [mcolors.to_hex(cmap(i)) for i in range(cmap.N)]
                else:
                    palette = cc.kbc[::-1]
                color_mapper = LogColorMapper(
                    palette = palette, 
                    low = min(self.source.data['color']), 
                    high = max(self.source.data['color'])
                    )
                glyphs = plot.scatter(
                    x = self.source.column_names[0],
                    y = self.source.column_names[-2],
                    source = self.source,
                    color = linear_cmap(
                        'color',
                        palette = palette,
                        low = min(self.source.data['color']),
                        high = max(self.source.data['color']),
                        ),
                    nonselection_alpha = 0.1,
                    selection_line_color = 'black',
                    selection_line_width = 0.5,
                    )
                color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0), width = 30)
                plot.add_layout(color_bar, 'right')

            else:
                glyphs = plot.scatter(
                    x = self.source.column_names[0],
                    y = self.source.column_names[-2],
                    color = self.source.column_names[-1],
                    nonselection_alpha = 0.1,
                    selection_line_color = 'black',
                    selection_line_width = 0.5,
                    source = self.source
                )

            self.glyphs = glyphs
            self.plot = plot
        else: 
            plot = figure(width = 500, height = 500, tools = "pan,lasso_select,box_select,tap,wheel_zoom,save,hover")
            self.plot = plot
            return
    
    def update_filterd_glyph(self, indices: list[int] = []):
        self.source.selected.indices = indices
    
    def update_glyph_by_color(self):
        self.glyphs = self.plot.scatter(
            x = self.source.column_names[0],
            y = self.source.column_names[-2],
            color = self.source.column_names[-1],
            nonselection_alpha = 0.1,
            selection_line_color = 'black',
            selection_line_width = 0.5,
            source = self.source
        )




class DiscretePlot:
    def __init__(self, base: Base):
        self.base = base
        self.widgets_dict = dict()
        self.init_widget_dict()
        self.plot_source = {'x': dict(), 'y': dict(), 'color': list()}
        self.plotter = ScatterPlot(False, None, self.get_source())
        self.widgets_dict['plot'] = self.plotter.plot
        self.layout = self.init_layout()
    
    def init_widget_dict(self):
        coordinates = self.get_coordinates()
        if self.base == Base.Cell:
            coordinates.remove('obs')
        elif self.base == Base.Gene:
            coordinates.remove('var')
        coordinates_select = make_widget(
            Widget_type.select,
            lambda: self.coordinates_select_callback(),
            options = coordinates,
            value = coordinates[0],
            title = 'Choose coordinate'
        )
        self.widgets_dict['coordinates_select'] = coordinates_select
        axes = self.get_axes()
        x_axis_select = make_widget(
            Widget_type.autocompleteInput,
            lambda: self.axis_select_callback(),
            completions = axes,
            value = axes[0],
            title = 'x_axis'
        )
        y_axis_select = make_widget(
            Widget_type.autocompleteInput,
            lambda: self.axis_select_callback(),
            completions = axes,
            min_characters = 1,
            value = axes[1],
            title = 'y_axis'
        )
        group_select = make_widget(
            Widget_type.select,
            lambda: self.group_select_callback(),
            options = [],
            value = '',
            title = 'Group by Variable:'
        )
        group_list = make_widget(
            Widget_type.checkBoxGroup,
            lambda: self.group_list_callback(),
            labels = ['unassigned'],
            active = [],
            title = 'group_list'
            )
        new_dict = {
            'x_axis_select': x_axis_select,
            'y_axis_select': y_axis_select,
            'group_select': group_select,
            'group_list': group_list
        }
        merged_dict = {**self.widgets_dict, **new_dict}
        self.widgets_dict = merged_dict
    
    def init_layout(self):
        coords_key = ['coordinates_select', 'x_axis_select', 'y_axis_select', 'group_select', 'group_list']
        layout_coords = make_layout(self.widgets_dict, coords_key, LayoutOrientation.vertical)
        wid_dict = self.widgets_dict
        wid_dict['layout_coords'] = layout_coords
        layout_key = ['plot', 'layout_coords']
        return(make_layout(wid_dict, layout_key, LayoutOrientation.horizontal))
    
    def coordinates_select_callback(self):
        pass

    def axis_select_callback(self):
        pass
    
    def group_select_callback(self):
        curgroup = self.widgets_dict['group_select'].value
        if self.base == Base.Cell:
            class_list = dt.adata.obs[curgroup]
        if self.base == Base.Gene:
            class_list = dt.adata.var[curgroup]
        unique_classes = list(set(class_list))
        class_to_color = {cls: color_list[i % len(color_list)] for i, cls in enumerate(unique_classes)}
        assigned_colors = [class_to_color[cls] for cls in class_list]
        self.plot_source['color'] = assigned_colors
        self.plotter.source = self.get_source()
        self.plotter.update_glyph_by_color()
        self.widgets_dict['plot'] = self.plotter.plot

    def group_list_callback(self):
        pass


    "functional"

    def get_coordinates(self):
        if self.base == Base.Cell:
            embedding = dt.adata.obsm_keys()
            label = ['obs']
        elif self.base == Base.Gene:
            embedding = dt.adata.varm_keys()
            label = ['var']
        return ['X'] + embedding + label
    
    def get_axes(self):
        coordinate = self.widgets_dict['coordinates_select'].value
        if coordinate == "X":
            if self.base == Base.Cell:
                return dt.adata.var_names.to_list()
            elif self.base == Base.Gene:
                return dt.adata.obs_names.to_list()
        else:
            if self.base == Base.Cell and coordinate in dt.adata.obsm_keys():
                if type(dt.adata.obsm[coordinate]) == np.ndarray:
                    axes = list()
                    for i in range(dt.adata.obsm[coordinate].shape[1]):
                        axes.append(f"coordinate_{i}")
                    return axes
                elif type(dt.adata.obsm[coordinate]) == pd.DataFrame:
                    return(dt.adata.obsm[coordinate].columns.to_list())
            elif self.base == Base.Gene and coordinate in dt.adata.varm_keys():
                if type(dt.adata.varm[coordinate]) == np.ndarray:
                    axes = list()
                    for i in range(dt.adata.varm[coordinate].shape[1]):
                        axes.append(f"coordinate_{i}")
                    return axes
                elif type(dt.adata.varm[coordinate]) == pd.DataFrame:
                    return(dt.adata.varm[coordinate].columns.to_list())
            # TODO: elif: sparse
        
    def get_source(self, selected : list | None = None):
        curmap = self.widgets_dict['coordinates_select'].value
        x_varname = self.widgets_dict['x_axis_select'].value
        y_varname = self.widgets_dict['y_axis_select'].value
        # if self.widgets_dict['is_log'].active == []:
        #     is_log = False
        #     is_exp = False
        # elif self.widgets_dict['is_log'].active == [0]: 
        #     is_log = True
        #     is_exp = False
        # elif self.widgets_dict['is_log'].active == [1]:
        #     is_log = False
        #     is_exp = True
        if curmap == 'X' and self.base == Base.Cell:
            if (x_varname in dt.adata.var.index.tolist()) and (y_varname in dt.adata.var.index.tolist()):
                x_index = dt.adata.var.index.get_loc(x_varname)
                y_index = dt.adata.var.index.get_loc(y_varname)
                if not issparse(dt.adata.X):
                    x_list = dt.adata.X[:, x_index]
                    y_list = dt.adata.X[:, y_index]
                else:
                    x_list = dt.adata.X.getcol(dt.adata.var_names.tolist().index(x_varname)).toarray().flatten()
                    y_list = dt.adata.X.getcol(dt.adata.var_names.tolist().index(y_varname)).toarray().flatten()  
            else: 
                print("Fatal: 'generic_columns' Plot.__get_source: variable not exist")
                return None
        elif curmap == 'X' and self.base == Base.Gene:
            if (x_varname in dt.adata.obs.index.tolist()) and (y_varname in dt.adata.obs.index.tolist()):
                x_index = dt.adata.obs.index.get_loc(x_varname)
                y_index = dt.adata.obs.index.get_loc(y_varname)
                if issparse(dt.adata.X):
                    x_list = dt.adata.X.getcol(dt.adata.obs_names.tolist().index(x_varname)).toarray().flatten()
                    y_list = dt.adata.X.getcol(dt.adata.obs_names.tolist().index(y_varname)).toarray().flatten()
                else: 
                    x_list = dt.adata.X[x_index, :]
                    y_list = dt.adata.X[y_index, :]    
            else: 
                print("Fatal: 'generic_columns' Plot.__get_source: variable not exist")
                return None
        # TODO: .layers, .obsm/.uns
        self.plot_source['x'].clear()
        self.plot_source['y'].clear()
        self.plot_source['x'][x_varname] = x_list
        self.plot_source['y'][y_varname] = y_list
        if self.plot_source['color'] == []:
            self.plot_source['color'] = [color_list[0]]*len(x_list)
        # TODO: color with obs_categorical
        source = ColumnDataSource(
            data = {
                list(self.plot_source['x'].keys())[0] : x_list,
                list(self.plot_source['y'].keys())[0] : y_list,
                'color': self.plot_source['color']
            }
        )
        if selected:
            source.selected.indices = selected
        return source
    
    # def get_cluster_list_prompt(self,
    #     active_cluster = None
    # ):
    #     """
    #     organize text of cluster checkbox by uns    
    #     return option list of cluster_checkbox
    #     """
    #     curgroup = self.widgets_dict['group_select'].value
    #     cluster_promtlist = []
    #     label_divlist = []
    #     active_prompt = None
    #     for cluster_name in dt.adata.uns['group_dict'][curgroup].index:
    #         cellnum = dt.adata.uns['group_dict'][curgroup].loc[cluster_name, 'cell_num']
    #         cluster_prompt = str(cluster_name) + ": cell_nums = " + str(cellnum)
    #         cluster_color = dt.adata.uns['group_dict'][curgroup].loc[cluster_name, 'color']
    #         cluster_label = Div (text = cluster_prompt, height = 8, style = {'color': cluster_color})
    #         label_divlist.append(cluster_label)
    #         cluster_promtlist.append(cluster_prompt)
    #         if cluster_name == active_cluster:
    #             active_prompt = cluster_prompt
    #     return cluster_promtlist, column(label_divlist, height = 30 * len(cluster_prompt)), active_prompt
    
    
    
    



class ContinuousPlot():
    def __init__(self, base: Base):
        self.base = base
        self.widgets_dict = dict()
        self.init_widget_dict()
        self.plot_source = {'x': dict(), 'y': dict(), 'color': list()}
        self.plotter = ScatterPlot(True, True, self.get_source())
        self.widgets_dict['plot'] = self.plotter.plot
        self.layout = self.init_layout()
    
    def init_widget_dict(self):
        coordinates = self.get_coordinates()
        if self.base == Base.Cell:
            label = 'obs'
        elif self.base == Base.Gene:
            label = 'var'
        coordinates_select = make_widget(
            Widget_type.select,
            lambda: self.coordinates_select_callback(),
            options = coordinates,
            value = coordinates[0],
            title = 'Choose coordinate'
        )
        self.widgets_dict['coordinates_select'] = coordinates_select
        axes = self.get_axes()
        x_axis_select = make_widget(
            Widget_type.autocompleteInput,
            lambda: self.axis_select_callback(),
            completions = axes,
            value = axes[0],
            title = 'x_axis'
        )
        y_axis_select = make_widget(
            Widget_type.autocompleteInput,
            lambda: self.axis_select_callback(),
            completions = axes,
            min_characters = 1,
            value = axes[1],
            title = 'y_axis'
        )
        coordinates.append(label)
        coordinates_select_mkr = make_widget(
            Widget_type.select,
            lambda: self.marker_select_callback(),
            options = coordinates,
            value = coordinates[0],
            title = 'Choose marker map'
        )
        self.widgets_dict['coordinates_select_mkr'] = coordinates_select_mkr
        axes_mkr = self.get_axes()
        marker_select_X = make_widget(
            Widget_type.autocompleteInput,
            lambda: self.markerX_select_callback(),
            completions = axes_mkr,
            min_characters = 1,
            value = axes_mkr[-1],
            title = 'marker'
        )
        if self.base == Base.Cell:
            if len(dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_obs.value]) > 0:
                axes_obsvar = dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_obs.value]
            else:
                axes_obsvar = ['no obs']
        if self.base == Base.Gene:
            if len(dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_var.value]) > 0:
                axes_obsvar = dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_var.value]
            else:
                axes_obsvar = ['no var']
        marker_select_obsvar = make_widget(
            Widget_type.select,
            options = axes_obsvar,
            value = axes_obsvar[0],
            title = 'marker'
        )
        new_dict = {
            'x_axis_select': x_axis_select,
            'y_axis_select': y_axis_select,
            'marker_select_X': marker_select_X,
            'marker_select_obsvar': marker_select_obsvar,
            'marker_select': marker_select_X
        }
        merged_dict = {**self.widgets_dict, **new_dict}
        self.widgets_dict = merged_dict
    
    def init_layout(self):
        coords_key = ['coordinates_select', 'x_axis_select', 'y_axis_select', 'coordinates_select_mkr', 'marker_select']
        layout_coords = make_layout(self.widgets_dict, coords_key, LayoutOrientation.vertical)
        wid_dict = self.widgets_dict
        wid_dict['layout_coords'] = layout_coords
        layout_key = ['plot', 'layout_coords']
        return(make_layout(wid_dict, layout_key, LayoutOrientation.horizontal))
    

    def coordinates_select_callback(self):
        pass

    def marker_select_callback(self):
        id_marker = self.widgets_dict['marker_select'].id
        if self.widgets_dict['coordinates_select_mkr'].value == 'X':
            self.widgets_dict['marker_select'] = self.widgets_dict['marker_select_X']
        elif self.widgets_dict['coordinates_select_mkr'].value in ['var', 'obs']:
            self.widgets_dict['marker_select'] = self.widgets_dict['marker_select_obsvar']
        refresh(id_marker, self.widgets_dict['marker_select'])
    
    def markerX_select_callback(self):
        pass

    def axis_select_callback(self):
        pass

    def get_coordinates(self):
        if self.base == Base.Cell:
            embedding = dt.adata.obsm_keys()
        elif self.base == Base.Gene:
            embedding = dt.adata.varm_keys()
        return ['X'] + embedding 
    
    def get_axes(self):
        coordinate = self.widgets_dict['coordinates_select'].value
        if coordinate == 'X':
            if self.base == Base.Cell:
                return dt.adata.var_names.to_list()
            elif self.base == Base.Gene:
                return dt.adata.obs_names.to_list()
        else:
            if self.base == Base.Cell and coordinate in dt.adata.obsm_keys():
                if type(dt.adata.obsm[coordinate]) == np.ndarray:
                    axes = list()
                    for i in range(dt.adata.obsm[coordinate].shape[1]):
                        axes.append(f"coordinate_{i}")
                    return axes
                elif type(dt.adata.obsm[coordinate]) == pd.DataFrame:
                    return(dt.adata.obsm[coordinate].columns.to_list())
            elif self.base == Base.Gene and coordinate in dt.adata.varm_keys():
                if type(dt.adata.varm[coordinate]) == np.ndarray:
                    axes = list()
                    for i in range(dt.adata.varm[coordinate].shape[1]):
                        axes.append(f"coordinate_{i}")
                    return axes
                elif type(dt.adata.varm[coordinate]) == pd.DataFrame:
                    return(dt.adata.varm[coordinate].columns.to_list())
            # TODO: elif: sparse

    def get_source(self, selected : list | None = None):
        curmap = self.widgets_dict['coordinates_select'].value
        x_varname = self.widgets_dict['x_axis_select'].value
        y_varname = self.widgets_dict['y_axis_select'].value
        # if self.widgets_dict['is_log'].active == []:
        #     is_log = False
        #     is_exp = False
        # elif self.widgets_dict['is_log'].active == [0]: 
        #     is_log = True
        #     is_exp = False
        # elif self.widgets_dict['is_log'].active == [1]:
        #     is_log = False
        #     is_exp = True
        if curmap == 'X' and self.base == Base.Cell:
            if (x_varname in dt.adata.var.index.tolist()) and (y_varname in dt.adata.var.index.tolist()):
                x_index = dt.adata.var.index.get_loc(x_varname)
                y_index = dt.adata.var.index.get_loc(y_varname)
                if not issparse(dt.adata.X):
                    x_list = dt.adata.X[:, x_index]
                    y_list = dt.adata.X[:, y_index]
                else:
                    x_list = dt.adata.X.getcol(dt.adata.var_names.tolist().index(x_varname)).toarray().flatten()
                    y_list = dt.adata.X.getcol(dt.adata.var_names.tolist().index(y_varname)).toarray().flatten()  
            else: 
                print("Fatal: 'generic_columns' Plot.__get_source: variable not exist")
                return None
        elif curmap == 'X' and self.base == Base.Gene:
            if (x_varname in dt.adata.obs.index.tolist()) and (y_varname in dt.adata.obs.index.tolist()):
                x_index = dt.adata.obs.index.get_loc(x_varname)
                y_index = dt.adata.obs.index.get_loc(y_varname)
                if issparse(dt.adata.X):
                    x_list = dt.adata.X.getcol(dt.adata.obs_names.tolist().index(x_varname)).toarray().flatten()
                    y_list = dt.adata.X.getcol(dt.adata.obs_names.tolist().index(y_varname)).toarray().flatten()
                else: 
                    x_list = dt.adata.X[x_index, :]
                    y_list = dt.adata.X[y_index, :]    
            else: 
                print("Fatal: 'generic_columns' Plot.__get_source: variable not exist")
                return None
        # TODO: .layers, .obsm/.uns
        self.plot_source['x'].clear()
        self.plot_source['y'].clear()
        self.plot_source['x'][x_varname] = x_list
        self.plot_source['y'][y_varname] = y_list
        self.plot_source['color'] = []
        colormap = self.widgets_dict['coordinates_select_mkr'].value
        marker = self.widgets_dict['marker_select'].value
        if colormap == 'X' and self.base == Base.Cell:
            color_var = dt.adata.var.index.get_loc(marker)
            if issparse(dt.adata.X):
                self.plot_source['color'] = dt.adata.X.getcol(color_var).toarray().flatten()
            else:
                self.plot_source['color'] = dt.adata.X[:, color_var]
        elif colormap == 'X' and self.base == Base.Gene:
            color_var = dt.adata.obs.index.get_loc(marker)
            if issparse(dt.adata.X):
                self.plot_source['color'] = dt.adata.X.getcol(color_var).toarray().flatten()
            else:
                self.plot_source['color'] = dt.adata.X[color_var, :]
        elif self.base == Base.Cell and colormap in dt.adata.obsm:
            self.plot_source['color'] = dt.adata.obsm[colormap][marker]
        elif self.base == Base.Gene and colormap in dt.adata.varm:
            self.plot_source['color'] = dt.adata.varm[colormap][marker]
        source = ColumnDataSource(
            data = {
                list(self.plot_source['x'].keys())[0] : x_list,
                list(self.plot_source['y'].keys())[0] : y_list,
                'color': self.plot_source['color']
            }
        )
        if selected:
            source.selected.indices = selected
        return source
        