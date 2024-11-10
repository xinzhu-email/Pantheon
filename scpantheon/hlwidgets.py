from bokeh.models import CheckboxGroup, AutocompleteInput, Select
from bokeh.layouts import row, column
from bokeh.io import curdoc
from widgets import Widgets
import data as dt
import tabs as tb

class Hlwidgets(Widgets):
    def __init__(self,
        name: str | None = 'generic columns',
    ):
        """
        dt.adata: handle with anndata structure  
        .obs: a pd.Dataframe with cell names as index, color and group name as columns  
        denotes a certain cell's current visualized color and which cluster it belongs to in each group  
        .uns: a dict {map_name: {group_name : pd.Dataframe}}  
        pd.Dataframe's index are cluster names, columns are color and cell_num  
        denotes each cluster's color and cell number
        """
        super().__init__(name)
        self.init_marker_map()
        self.init_marker()
        super().init_tab()
    
    def init_marker_map(self):
        map_list = dt.adata.obsm_keys() + ['generic_columns'] 
        marker_map = Select(
            title = 'Marker map:',
            value = map_list[0],
            options = map_list
        )
        marker_map.on_change('value',lambda attr, old, new :self.update_marker_map(attr, old, new))
        widgets_dict = {'marker_map' : marker_map}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
    
    def init_marker(self):
        varlist = super().get_var(isMarker = True)
        marker = AutocompleteInput(
            title = "marker:", 
            value = varlist[0], 
            completions = varlist, 
            min_characters = 1
        )
        marker.on_change("value", lambda attr, old, new : self.update_marker(attr, old, new))
        widgets_dict = {'marker' : marker}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
    
    def update_marker_map(self, attr, old, new):
        tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        def update_marker_map_next(self):
            self.init_marker()
            self.update_plot_source_by_colors()
            self.plot_coordinates()
            self.update_layout()
            self.view_tab()
            tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        curdoc().add_next_tick_callback(lambda : update_marker_map_next(self))

    def update_marker(self,attr, old, new):
        tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        def update_marker_next(self):
            self.update_plot_source_by_colors()
            self.plot_coordinates()
            self.update_layout()
            self.view_tab()
            tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        curdoc().add_next_tick_callback(lambda : update_marker_next(self))

    def update_plot_source_by_colors(self):
        self.plot_source['color'] = []
        marker_map = self.widgets_dict['marker_map'].value
        marker = self.widgets_dict['marker'].value
        print(marker_map)
        if marker_map == 'generic_columns':
            if 'X' in dt.adata.uns['sparse']:
                self.plot_source['color'] = dt.adata.X.getcol(dt.adata.var_names.tolist().index(marker)).toarray().flatten()
            else:
                for cell_name in dt.adata.X.index:
                    self.plot_source['color'].append(dt.adata.X.loc[cell_name, marker]) 
        else:
            for cell_name in dt.adata.obs_names:
                self.plot_source['color'].append(dt.adata.obsm[marker_map].loc[cell_name, marker])

    def update_layout(self):
        coords_key = ['choose_map', 'x_varname', 'y_varname', 'is_log', 'log_info', 'marker_map', 'marker'] 
        values = [self.widgets_dict[key] for key in coords_key if key in self.widgets_dict]
        layout_coords = column(values)
        self.layout = row([self.figure.plot, layout_coords])