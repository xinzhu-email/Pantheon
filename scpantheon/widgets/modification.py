from scpantheon.buttons import Widget_type, LayoutOrientation, make_widget, make_layout
from scpantheon.base import Base
from scpantheon.widgets.plot import color_list, DiscretePlot, ContinuousPlot
from scpantheon.widgets.filter import Filter
from bokeh.models import ColorPicker
from scpantheon.stdata import DataCat
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
        
        if self.base == Base.Cell:
            cat_list = dt.adata.obs_keys()
            if len(cat_list) == 0:
                cat_list = ["no obs"]
            string_base = "Obs"
        elif self.base == Base.Gene:
            cat_list = dt.adata.var_keys()
            if len(cat_list) == 0:
                cat_list = ["no var"]
            string_base = "Var"
        
        self.widgets_dict['categorizor'] = make_widget(Widget_type.div, text = f"<div style='font-size: 30px;'> {string_base} Categorizor")
        
        self.widgets_dict['cat_list'] = make_widget(
            Widget_type.select,
            lambda: self.cat_select(),
            options = cat_list,
            title = f"{string_base} list",
            value = cat_list[0]
        )
        self.widgets_dict['cat_category'] = make_widget(
            Widget_type.radioButtonGroup,
            labels = [f"{string_base} categorical", f"{string_base} data"],
            active = 0,
        )
        self.widgets_dict['cat_categorize'] = make_widget(
            Widget_type.button,
            lambda: self.cat_categorize(),
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
        categorize_layout = make_layout(self.widgets_dict, ['categorizor', 'cat_list', 'cat_category', 'cat_categorize']) 
        operation_layout = make_layout([modify_layout, categorize_layout, filter_complete], orientation = LayoutOrientation.horizontal)
        plot_layout = make_layout([self.plot_dis.layout, self.plot_con.layout], orientation = LayoutOrientation.horizontal)
        return make_layout([plot_layout, operation_layout])


    
    
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

    def cat_select(self):
        pass

    def cat_categorize(self):
        is_data = self.widgets_dict['cat_category'].active
        obsvar = self.widgets_dict['cat_list'].value
        ori_con_value = self.plot_con.widgets_dict['marker_select_obsvar'].value
        ori_dis_value = self.plot_dis.widgets_dict['group_select'].value
        if is_data == 0:
            if self.base == Base.Cell:
                if obsvar in dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_obs.value]:
                    return
                else:
                    if obsvar in dt.adata.uns["scpantheon_categorizor"][DataCat.Data_obs.value]:
                        dt.adata.uns["scpantheon_categorizor"][DataCat.Data_obs.value].remove(obsvar)
                        if ori_con_value == obsvar:
                            if len(dt.adata.uns["scpantheon_categorizor"][DataCat.Data_obs.value]) > 0:
                                self.plot_con.widgets_dict['marker_select_obsvar'].options = dt.adata.uns["scpantheon_categorizor"][DataCat.Data_obs.value]
                                self.plot_con.widgets_dict['marker_select_obsvar'].value = dt.adata.uns["scpantheon_categorizor"][DataCat.Data_obs.value][0]
                            else:
                                self.plot_con.widgets_dict['marker_select_obsvar'].options = ['no obs'] 
                                self.plot_con.widgets_dict['marker_select_obsvar'].value = 'no obs'
                    dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_obs.value].append(obsvar)
                    self.plot_dis.widgets_dict['group_select'].options = dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_obs.value]
                    self.plot_dis.widgets_dict['group_select'].value = obsvar
            if self.base == Base.Gene:
                if obsvar in dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_var.value]:
                    return
                else:
                    if obsvar in dt.adata.uns["scpantheon_categorizor"][DataCat.Data_var.value]:
                        dt.adata.uns["scpantheon_categorizor"][DataCat.Data_var.value].remove(obsvar)
                        self.plot_con.widgets_dict['marker_select_obsvar'].options = dt.adata.uns["scpantheon_categorizor"][DataCat.Data_var.value]
                        if ori_con_value == obsvar:
                            if len(dt.adata.uns["scpantheon_categorizor"][DataCat.Data_var.value]) > 0:
                                self.plot_con.widgets_dict['marker_select_obsvar'].options = dt.adata.uns["scpantheon_categorizor"][DataCat.Data_var.value]
                                self.plot_con.widgets_dict['marker_select_obsvar'].value = dt.adata.uns["scpantheon_categorizor"][DataCat.Data_var.value][0]
                            else:
                                self.plot_con.widgets_dict['marker_select_obsvar'].options = ['no var'] 
                                self.plot_con.widgets_dict['marker_select_obsvar'].value = 'no var'
                    dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_var.value].append(obsvar)
                    self.plot_dis.widgets_dict['group_select'].options = dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_var.value]
                    self.plot_dis.widgets_dict['group_select'].value = obsvar
        elif is_data == 1:
            if self.base == Base.Cell:
                if obsvar in dt.adata.uns["scpantheon_categorizor"][DataCat.Data_obs.value]:
                    return
                else:
                    if obsvar in dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_obs.value]:
                        dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_obs.value].remove(obsvar)
                        if ori_dis_value == obsvar:
                            if len(dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_obs.value]) > 0:
                                self.plot_dis.widgets_dict['group_select'].options = dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_obs.value]
                                self.plot_dis.widgets_dict['group_select'].value = dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_obs.value][0]
                            else:
                                self.plot_dis.widgets_dict['group_select'].options = ['no obs'] 
                                self.plot_dis.widgets_dict['group_select'].value = 'no obs'
                    dt.adata.uns["scpantheon_categorizor"][DataCat.Data_obs.value].append(obsvar)
                    self.plot_con.widgets_dict['marker_select_obsvar'].options = dt.adata.uns["scpantheon_categorizor"][DataCat.Data_obs.value]
                    self.plot_con.widgets_dict['marker_select_obsvar'].value = obsvar
            if self.base == Base.Gene:
                if obsvar in dt.adata.uns["scpantheon_categorizor"][DataCat.Data_var.value]:
                    return
                else:
                    if obsvar in dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_var.value]:
                        dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_var.value].remove(obsvar)
                        if ori_dis_value == obsvar:
                            if len(dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_var.value]) > 0:
                                self.plot_dis.widgets_dict['group_select'].options = dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_var.value]
                                self.plot_dis.widgets_dict['group_select'].value = dt.adata.uns["scpantheon_categorizor"][DataCat.Catagorial_var.value][0]
                            else:
                                self.plot_dis.widgets_dict['group_select'].options = ['no var'] 
                                self.plot_dis.widgets_dict['group_select'].value = 'no var'
                    dt.adata.uns["scpantheon_categorizor"][DataCat.Data_var.value].append(obsvar)
                    self.plot_con.widgets_dict['marker_select_obsvar'].options = dt.adata.uns["scpantheon_categorizor"][DataCat.Data_var.value]
                    self.plot_con.widgets_dict['marker_select_obsvar'].value = obsvar
    



    """functional"""
    def get_group_list(self):
        # TODO: read directly from scp_adata
        return ['catagorical_var/obs_0', 'catagorical_var/obs_1']