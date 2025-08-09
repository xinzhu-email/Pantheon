from enum import Enum
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from scpantheon.base import Base
from scpantheon.buttons import make_layout, make_widget, Widget_type
from scpantheon.stdata import DataCat, ExtInfo
import stdata as dt

class Stage(Enum):
    PREREQUISITE = "Prerequisite"
    RESULT = "Result"

class Layer:
    def __init__(self, top_x: float, top_y: float, width: float, height: float, top_label: str, base_color, highlight_color, is_highlight: bool, n_layer: int):
        if n_layer == 1:
            print("class Layer require n_layer > 1, if n_layer is 1, call class Table")
        self.x_list = [top_x - (n_layer - i - 1) * 0.03 for i in range(n_layer)]
        self.y_list = [top_y - (n_layer - i - 1) * 0.03 for i in range(n_layer)]
        self.width = [width] * n_layer
        self.height = [height] * n_layer
        self.text = [""] * (n_layer - 1) + [top_label]
        self.base_color = base_color
        self.highlight_color = highlight_color
        if is_highlight:
            self.colors = [base_color] * (n_layer - 1) + [self.highlight_color]
        else:
            self.colors = [base_color] * n_layer
    
    def update_color(self, is_highlight: bool):
        if is_highlight:
            self.colors[-1] = self.highlight_color
        else:
            self.colors[-1] = self.base_color


class Table:
    def __init__(self, plot_base, x_base, y_base, cat_width, cat_height, val_width_height, highlight_width_hight, highlight_shift, is_categorical, is_value, cat_base_color, val_base_color, highlight_color):
        self.x_list = list()
        self.y_list = list()
        self.width = list()
        self.height = list()
        self.text = list()
        self.colors = list()
        if plot_base == Base.Cell:
            self.height = [cat_height] * 2
            self.width = [cat_width, val_width_height]
            self.y_list = [y_base] * 2
            self.x_list = [x_base, x_base + cat_width/2 + val_width_height/2]
            self.text = ["obs\ncategorial", "obs\nvalue"]
            self.colors = [cat_base_color, val_base_color]
            if is_categorical:
                self.height.append(cat_height)
                self.width.append(highlight_width_hight)
                self.y_list.append(y_base)
                self.x_list.append(x_base - cat_width/2 + highlight_shift + highlight_width_hight/2)
                self.text.append("")
                self.colors.append(highlight_color)
            if is_value:
                self.height.append(cat_height)
                self.width.append(highlight_width_hight)
                self.y_list.append(y_base)
                self.x_list.append(x_base + cat_width/2 + highlight_shift + highlight_width_hight/2)
                self.text.append("")
                self.colors.append(highlight_color)
        if plot_base == Base.Gene:
            self.height = [cat_height, val_width_height]
            self.width = [cat_width] * 2
            self.y_list = [y_base, y_base + cat_height/2 + val_width_height/2]
            self.x_list = [x_base] * 2
            self.text = ["var categorial", "var value"]
            self.colors = [cat_base_color, val_base_color]
            if is_categorical:
                self.height.append(highlight_width_hight)
                self.width.append(cat_width)
                self.y_list.append(y_base - cat_height/2 + highlight_shift + highlight_width_hight/2)
                self.x_list.append(x_base)
                self.text.append("")
                self.colors.append(highlight_color)
            if is_value:
                self.height.append(highlight_width_hight)
                self.width.append(cat_width)
                self.y_list.append(y_base + cat_height/2 + highlight_shift + highlight_width_hight/2)
                self.x_list.append(x_base)
                self.text.append("")
                self.colors.append(highlight_color)



class AdataVis:
    def __init__(
            self, 
            stage: Stage, 
            active: list[DataCat] | None = []):
        self.p = figure()
        if stage == Stage.PREREQUISITE:
            self.title = make_widget(Widget_type.div, text = f"<div style='font-size: 25px;'>Highlighted Data Required by Current Extension Session")
        elif stage == Stage.RESULT:
            self.title = make_widget(Widget_type.div, text = f"<div style='font-size: 25px;'>Highlighted Data Produced by Current Extension Session")
        self.active = active
        kwarg_layers = {
            "top_x": 2.25, "top_y": 2.5, "width": 1, "height": 0.75, "top_label": "X/Layers", 
            "base_color": "#6a51a3", "highlight_color": "#bcbddc", "is_highlight": False, "n_layer": 3
        }
        kwarg_obsp = {
            "top_x": 0.5, "top_y": 2.5, "width": 0.75, "height": 0.75, "top_label": "obsp", 
            "base_color": "#3182bd", "highlight_color": "#9ecae1", "is_highlight": False, "n_layer": 2
        }
        kwarg_obsm = {
            "top_x": 1.325, "top_y": 2.5, "width": 0.5, "height": 0.75, "top_label": "obsm", 
            "base_color": "#006400", "highlight_color": "#90ee90", "is_highlight": False, "n_layer": 4
        }
        kwarg_varm = {
            "top_x": 2.25, "top_y": 1.75, "width": 1, "height": 0.5, "top_label": "varm", 
            "base_color": "#ae017e", "highlight_color": "#fee0e0", "is_highlight": False, "n_layer": 2
        }
        kwarg_varp = {
            "top_x": 2.25, "top_y": 0.9, "width": 1, "height": 1, "top_label": "varp", 
            "base_color": "#d94801", "highlight_color": "#fee6ce", "is_highlight": False, "n_layer": 3
        }
        kwarg_uns = {
            "top_x": 0.8, "top_y": 1.2, "width": 1.2, "height": 1, "top_label": "uns", 
            "base_color": "#bdb76b", "highlight_color": "#ffff00", "is_highlight": False, "n_layer": 3
        }
        self.kwarg_obs = {
            "plot_base": Base.Cell, "x_base": 3.15, "y_base": 2.5, "cat_width": 0.55, "cat_height": 0.75, "val_width_height": 0.35, 
            "highlight_width_hight": 0.05, "highlight_shift": 0, "is_categorical": False, "is_value": False, 
            "cat_base_color": "#ff4500", "val_base_color": "#ff8c00", "highlight_color": "#ffd700"
        }
        self.kwarg_var = {
            "plot_base": Base.Gene, "x_base": 2.25, "y_base": 3.2, "cat_width": 1, "cat_height": 0.35, "val_width_height": 0.35, 
            "highlight_width_hight": 0.05, "highlight_shift": 0, "is_categorical": False, "is_value": False, 
            "cat_base_color": "#6baed6", "val_base_color": "#4292c6", "highlight_color": "#deebf7"
        }
        for datatype in self.active:
            match datatype:
                case DataCat.EXPMATRIX:
                    kwarg_layers["is_highlight"] = True
                case DataCat.HDCoordinate:
                    kwarg_layers["is_highlight"] = True
                case DataCat.LDCoordinate_var:
                    kwarg_varm["is_highlight"] = True
                case DataCat.LDCoordinate_obs:
                    kwarg_obsm["is_highlight"] = True
                case DataCat.Catagorial_var:
                    self.kwarg_var["is_categorical"] = True
                case DataCat.Catagorial_obs:
                    self.kwarg_obs["is_categorical"] = True
                case DataCat.Data_var:
                    self.kwarg_var["is_value"] = True
                case DataCat.Data_obs:
                    self.kwarg_obs["is_value"] = True
                case DataCat.Pairwise_var:
                    kwarg_varp["is_highlight"] = True
                case DataCat.Pairwise_obs:
                    kwarg_obsp["is_highlight"] = True
                case DataCat.Unstructured:
                    kwarg_uns["is_highlight"] = True
        
        self.layers = Layer(**kwarg_layers)
        self.obsp = Layer(**kwarg_obsp)
        self.obsm = Layer(**kwarg_obsm)
        self.obs = Table(**self.kwarg_obs)
        self.varm = Layer(**kwarg_varm)
        self.varp = Layer(**kwarg_varp)
        self.var = Table(**self.kwarg_var)
        self.uns = Layer(**kwarg_uns)
        self.layout = self.init_layout()


    def init_layout(self):
        data = {
            'x': self.obsp.x_list + self.obsm.x_list + self.layers.x_list + self.varm.x_list + self.varp.x_list + self.obs.x_list + self.var.x_list + self.uns.x_list,
            'y': self.obsp.y_list + self.obsm.y_list + self.layers.y_list + self.varm.y_list + self.varp.y_list + self.obs.y_list + self.var.y_list + self.uns.y_list,
            'width': self.obsp.width + self.obsm.width + self.layers.width + self.varm.width + self.varp.width + self.obs.width + self.var.width + self.uns.width,
            'height': self.obsp.height + self.obsm.height + self.layers.height + self.varm.height + self.varp.height + self.obs.height + self.var.height + self.uns.height,
            'color': self.obsp.colors + self.obsm.colors + self.layers.colors + self.varm.colors + self.varp.colors + self.obs.colors + self.var.colors + self.uns.colors,
            'text': self.obsp.text + self.obsm.text + self.layers.text + self.varm.text + self.varp.text + self.obs.text + self.var.text + self.uns.text
        }
        source = ColumnDataSource(data)

        self.p = figure(width=500, height=500,
                x_range=(0, 4), y_range=(0, 4),
                toolbar_location=None,
                outline_line_color=None,
                background_fill_color=None,
                border_fill_color=None)
        self.p.axis.visible = False
        self.p.grid.visible = False
        self.p.toolbar.logo = None
        self.p.rect('x', 'y', 'width', 'height', fill_color='color', line_color="black", source=source)
        self.p.text('x', 'y', text='text', text_font_size="12px",
            text_align="center", text_baseline="middle",
            source=source)
        return make_layout([self.title, self.p])
    
    def update_active(self, active: list[DataCat]):
        if DataCat.EXPMATRIX in active or DataCat.HDCoordinate in active:
            self.layers.update_color(True)
        else:
            self.layers.update_color(False)
        if DataCat.LDCoordinate_obs in active:
            self.obsm.update_color(True)
        else:
            self.obsm.update_color(False)
        if DataCat.LDCoordinate_var in active:
            self.varm.update_color(True)
        else:
            self.varm.update_color(False)
        if DataCat.Pairwise_obs in active:
            self.obsp.update_color(True)
        else:
            self.obsp.update_color(False)
        if DataCat.Pairwise_var in active:
            self.varp.update_color(True)
        else:
            self.varp.update_color(False)
        if DataCat.Unstructured in active:
            self.uns.update_color(True)
        else:
            self.uns.update_color(False)
        if DataCat.Catagorial_obs in active:
            self.kwarg_obs["is_categorical"] = True
        else:
            self.kwarg_obs["is_categorical"] = False
        if DataCat.Catagorial_var in active:
            self.kwarg_var["is_categorical"] = True
        else:
            self.kwarg_var["is_categorical"] = False
        if DataCat.Data_obs in active:
            self.kwarg_obs["is_value"] = True
        else:
            self.kwarg_obs["is_value"] = False
        if DataCat.Data_var in active:
            self.kwarg_var["is_value"] = True
        else:
            self.kwarg_var["is_value"] = False
        self.obs = Table(**self.kwarg_obs)
        self.var = Table(**self.kwarg_var)
        self.layout = self.init_layout()    

# STREAMLINE_2_INT: dict = {
#     'raw': 0, 'quality_control': 1, 'norm': 2, 'gene_analysis': 3,
#     'imputation': 4, 'dimensionality_reduction': 5, 'clustering': 6,
#     'trajectory': 7, 'de': 8, 'grn': 9, 'cell_communication': 10
# }


    
class Tracker:
    def __init__(self):
        title = make_widget(Widget_type.div, text = "<div style='font-size: 25px;'>Session Tracker")
        dt.digplot.add_node(ExtInfo("raw", "raw")) 
        dt.digplot.update_node_valid("raw", dt.adata.var_names, dt.adata.obs_names)
        dt.digplot.update_node_by_dataframe(
            "raw", 
            dt.session_info, 
            results = True, 
            resultlist = "X"
        )
        dt.digplot.make_plot()
        self.layout = make_layout([title, dt.digplot.plot])
