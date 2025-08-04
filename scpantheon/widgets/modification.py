from scpantheon.buttons import Widget_type, LayoutOrientation, make_widget, make_layout
from scpantheon.base import Base
from scpantheon.widgets.plot import color_list, DiscretePlot, ContinuousPlot
from scpantheon.widgets.filter import Filter
from bokeh.models import ColorPicker
import stdata as dt

class Modification:
    def __init__(self, base: Base):
        self.base = base
        self.widgets_dict = dict()
        self.init_widget_dict()
        self.layout = self.init_layout()
    
    def init_widget_dict(self):
        self.widgets_dict['title'] = make_widget(Widget_type.div, text = f"<div style='font-size: 30px;'> Manual Adjustment for {self.base.value}")
        self.widgets_dict['group_name'] = make_widget(Widget_type.text, title = 'Input Group Name: ')
        self.widgets_dict['group_create'] = make_widget(
            Widget_type.button,
            lambda : self.create_group_callback(),
            label = 'Create Group'
        )
        self.widgets_dict['group_rename'] = make_widget(
            Widget_type.button,
            lambda : self.rename_group_callback(),
            label = 'Rename Group'
        )
        self.widgets_dict['group_delete'] = make_widget(
            Widget_type.button,
            lambda : self.delete_group_callback(),
            label = 'Delete Group'
        )
        self.widgets_dict['cluster_name'] = make_widget(Widget_type.text, title = 'Input Cluster Name: ')
        self.widgets_dict['cluster_create'] = make_widget(
            Widget_type.button,
            lambda : self.create_cluster_callback(),
            label = 'Create Cluster'
        )
        self.widgets_dict['cluster_rename'] = make_widget(
            Widget_type.button,
            lambda : self.rename_cluster_callback(),
            label = 'Rename Cluster'
        )
        self.widgets_dict['cluster_delete'] = make_widget(
            Widget_type.button,
            lambda : self.delete_cluster_callback(),
            label = 'Delete Cluster'
        )
        self.widgets_dict['cluster_merge'] = make_widget(
            Widget_type.button,
            lambda : self.merge_cluster_callback(),
            label = 'Merge Cluster'
        )
        self.widgets_dict['add_to'] = make_widget(
            Widget_type.button,
            lambda : self.add_to_callback(),
            label = f"Add {self.base.value} to Selected Cluster"
        )
        self.widgets_dict['remove_from'] = make_widget(
            Widget_type.button,
            lambda : self.remove_from_callback(),
            label = f"Remove {self.base.value} from Selected Clusters"
        )
        self.widgets_dict['update'] = make_widget(
            Widget_type.button,
            lambda : self.update_callback(),
            label = f"Update Selected Cluster by Selected {self.base.value}"
        )
        self.widgets_dict['color_picker'] = ColorPicker(
            title = "Select color:",
            color = color_list[0], 
            css_classes = color_list
        )
        self.widgets_dict['change_color'] = make_widget(
            Widget_type.button,
            lambda : self.change_color_callback(),
            label = "Change Cluster Color"
        )
        self.widgets_dict['categorizor'] = make_widget(Widget_type.div, text = f"<div style='font-size: 30px;'> Obs/Var Categorizor")
        
        obs_list = dt.adata.obs_keys()
        if len(obs_list) == 0:
            obs_list = ["no obs"]
        var_list = dt.adata.var_keys()
        if len(var_list) == 0:
            var_list = ["no var"]
        self.widgets_dict['obs_list'] = make_widget(
            Widget_type.select,
            lambda: self.obs_select(),
            options = obs_list,
            title = "obs list",
            value = obs_list[0]
        )
        self.widgets_dict['obs_category'] = make_widget(
            Widget_type.radioButtonGroup,
            labels = ['obs categorical', 'obs data'],
            active = 0,
        )
        self.widgets_dict['obs_categorize'] = make_widget(
            Widget_type.button,
            lambda: self.obs_categorize(),
            label = "catagorize"
        )
        self.widgets_dict['var_list'] = make_widget(
            Widget_type.select,
            lambda: self.var_select(),
            options = var_list,
            title = "var list",
            value = var_list[0]
        )
        self.widgets_dict['var_category'] = make_widget(
            Widget_type.radioButtonGroup,
            labels = ['var categorical', 'var data'],
            active = 0
        )
        self.widgets_dict['var_categorize'] = make_widget(
            Widget_type.button,
            lambda: self.var_categorize(),
            label = "catagorize"
        )
        self.plot_dis = DiscretePlot(self.base)
        self.plot_con = ContinuousPlot(self.base)
        self.filter = Filter(self.base)
        self.filter_confirm = make_widget(
            Widget_type.button,
            lambda: self.filter_confirm_callback(),
            label = f"confirm {self.base.value} selection"
        )
    
    def init_layout(self):
        group_layout = make_layout(self.widgets_dict, ['group_name', 'group_create', 'group_rename', 'group_delete'])
        cluster_layout = make_layout(self.widgets_dict, ['cluster_name', 'cluster_create', 'cluster_rename', 'cluster_merge', 'cluster_delete'])
        annotation_layout = make_layout(self.widgets_dict, ['add_to', 'remove_from', 'update', 'color_picker', 'change_color'])
        function_layout = make_layout([group_layout, cluster_layout, annotation_layout], orientation = LayoutOrientation.horizontal)
        modify_layout = make_layout([self.widgets_dict['title'], function_layout])
        filter_complete = make_layout([self.filter.layout, self.filter_confirm])
        obs_categorize = make_layout(self.widgets_dict, ['obs_list', 'obs_category', 'obs_categorize'])
        var_categorize = make_layout(self.widgets_dict, ['var_list', 'var_category', 'var_categorize'])
        obsvar_categorize = make_layout([obs_categorize, var_categorize], orientation = LayoutOrientation.horizontal)
        categorize_layout = make_layout([self.widgets_dict['categorizor'], obsvar_categorize]) 
        operation_layout = make_layout([modify_layout, filter_complete], orientation = LayoutOrientation.horizontal)
        plot_layout = make_layout([self.plot_dis.layout, self.plot_con.layout], orientation = LayoutOrientation.horizontal)
        return make_layout([plot_layout, operation_layout, categorize_layout])


    
    
    """callback"""
    def create_group_callback(self):
        pass

    def rename_group_callback(self):
        pass

    def delete_group_callback(self):
        pass

    def select_group_callback(self):
        pass

    def create_cluster_callback(self):
        pass

    def rename_cluster_callback(self):
        pass

    def delete_cluster_callback(self):
        pass

    def merge_cluster_callback(self):
        pass

    def add_to_callback(self):
        pass

    def remove_from_callback(self):
        pass

    def update_callback(self):
        pass

    def change_color_callback(self):
        pass    

    def filter_confirm_callback(self):
        indices = list(set(self.plot_con.plotter.source.selected.indices) | set(self.plot_dis.plotter.source.selected.indices))
        if self.base == Base.Cell:
            if indices == []:
                indices = list(range(dt.adata.n_obs))
            dt.validcache.update_valid_obs(indices)
        if self.base == Base.Gene:
            if indices == []:
                indices = list(range(dt.adata.n_vars))
            dt.validcache.update_valid_var(indices)
        self.plot_con.plotter.update_filterd_glyph(indices)
        self.plot_dis.plotter.update_filterd_glyph(indices)

    def obs_select(self):
        pass

    def var_select(self):
        pass

    def obs_categorize(self):
        obs_to_categorial = self.widgets_dict['obs_list'].value
        self.plot_dis.update_categorical_by_categorizor(obs_to_categorial)

    def var_categorize(self):
        pass



    """functional"""
    def get_group_list(self):
        # TODO: read directly from scp_adata
        return ['catagorical_var/obs_0', 'catagorical_var/obs_1']