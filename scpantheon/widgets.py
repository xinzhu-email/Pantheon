from bokeh.models import Select, Button, CheckboxGroup, TextInput, ColorPicker, AutocompleteInput, ColumnDataSource, Div
from bokeh.layouts import row, column
from myplot import Plot
import data as dt
import tabs as tb
import numpy as np

class Widgets:
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
        self.new_panel = True
        self.name = name
        self.widgets_dict = dict()
        self.plot_source = {'x': dict(), 'y': dict(), 'color': list()}
        self.figure = Plot()
        self.layout = None
        self.init_map()
        self.init_coordinates()
        self.update_plot_source_by_coords()
        self.init_group()
        self.init_group_select()
        self.init_color()
        self.init_cluster()
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()
    
    def switch_tab(self):
        """
        when the tab already exists, update itself by adata
        """
        curmap = self.widgets_dict['choose_map'].value
        curgroup = self.widgets_dict['group_select'].value
        self.init_map(curmap)
        self.init_coordinates()
        self.update_plot_source_by_coords()
        self.init_group_select(curgroup)
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()

    """
    Following are functions to init widgets in homepage
    """    
    def init_map(self,
        map_name: str | None = None
    ):
        """
        Init widget 'Choose map' according to adata.obsm
        """
        map_list = dt.adata.obsm_keys() + ['generic_columns']
        if not map_name:
            map_name = map_list[0]
        elif map_name not in map_list:
            print("Error: original map is no longer in the new maplist")
            map_name = map_list[0]
        choose_map = Select(
            title = 'Choose map:',
            value = map_name,
            options = map_list
        )
        choose_map.on_change('value',lambda attr, old, new :self.update_var())
        widgets_dict = {'choose_map' : choose_map}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
    
    def init_coordinates(self):
        """
        init x_axis, y_axis and log checkbox
        """
        varlist = self.get_var()
        if 'is_log' in self.widgets_dict:
            active_status = self.widgets_dict['is_log'].active
        else:
            active_status = []
        x_axis = AutocompleteInput(
            title = "x axis:", 
            value = varlist[0], 
            completions = varlist, 
            min_characters = 1
        )
        x_axis.on_change("value", lambda attr, old, new : self.update_axis('x_varname', attr, old, new))

        y_axis = AutocompleteInput(
            title = "y axis:", 
            value = varlist[1], 
            completions = varlist, 
            min_characters = 1
        )
        y_axis.on_change("value", lambda attr, old, new : self.update_axis('y_varname', attr, old, new))

        log_axis = CheckboxGroup(labels = ['Log-scaled axis', 'Exponential-scaled axis'], active = active_status)
        log_axis.on_change('active',lambda attr, old, new : self.update_log(attr, old, new))

        log_status = self.get_log_status()
        log_info = Div(text = log_status)

        widgets_dict = {'x_varname': x_axis, 'y_varname': y_axis, 'is_log': log_axis, 'log_info': log_info}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict       
    
    def init_group(self):
        """
        init fixed group buttons   
        group_select inited alone afterwards as it depends on other group buttons
        """    
        group_name = TextInput (title = 'Input Group Name: ', value = '')
        
        create_group = Button(label = 'Create Group')
        create_group.on_click(lambda : self.create_group_select())

        rename_group = Button(label = 'Rename Group')
        rename_group.on_click(lambda : self.rename_group_select())

        delete_group = Button(label = 'Delete Group')
        delete_group.on_click(lambda : self.delete_group_select())

        widgets_dict = {
            'group_name' : group_name,
            'create_group': create_group,
            'rename_group': rename_group,
            'delete_group': delete_group
        }
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
    
    def init_group_select(self,
        group_name: str | None = None
    ):
        """
        init group select according to uns
        """
        grouplist = list(dt.adata.uns['group_dict'].keys())
        grouplist.remove('Please create a group')
        if grouplist == []:
            grouplist.append('Please create a group')
        if group_name in grouplist:
            group_select_value = group_name
        else:
            group_select_value = grouplist[-1]
        group_select = Select(
            title='Select Cluster Group:',
            options = grouplist,
            value = group_select_value
        )
        group_select.on_change("value", lambda attr, old, new : self.update_group())
        widgets_dict = {'group_select' : group_select}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
    
    def init_color(self):
        """
        init color_picker without any callback
        """
        color_picker = ColorPicker(
            title = "Select color:",
            color = dt.color_list[0], 
            css_classes = dt.color_list
        )
        widgets_dict = {'color_picker' : color_picker}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
    
    def init_cluster(self):
        """
        init fixed cluster buttons   
        cluster_select inited alone afterwards as it depends on other cluster buttons
        """  
        cluster_name = TextInput (title = 'Input Cluster Name: ', value = '')
        
        create_cluster = Button(label = 'Create Cluster')
        create_cluster.on_click(lambda : self.create_cluster_select())

        rename_cluster = Button(label = 'Rename Cluster')
        rename_cluster.on_click(lambda : self.rename_cluster_select())

        delete_cluster = Button(label = 'Delete Cluster')
        delete_cluster.on_click(lambda : self.delete_cluster_select())

        merge_cluster = Button(label = 'Merge Cluster')
        merge_cluster.on_click(lambda : self.merge_cluster_select())

        add_to = Button(label = 'Add to')
        add_to.on_click(lambda : self.add_to())

        remove_from = Button(label = 'Remove from')
        remove_from.on_click(lambda : self.remove_from())

        update = Button(label = 'Update Cluster')
        update.on_click(lambda : self.update())

        change_cluster_color = Button(label = 'Change Cluster Color')
        change_cluster_color.on_click(lambda : self.change_cluster_color())

        widgets_dict = {
            'cluster_name' : cluster_name,
            'create_cluster': create_cluster,
            'rename_cluster': rename_cluster,
            'delete_cluster': delete_cluster,
            'merge_cluster': merge_cluster,
            'add_to' : add_to,
            'remove_from': remove_from,
            'update' : update,
            'change_cluster_color' : change_cluster_color
        }
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
    
    def init_cluster_select(self):
        """
        init cluster_checkbox according to uns
        """
        clusterlist = self.get_cluster_list()
        cluster_checkbox = CheckboxGroup(
            labels = clusterlist,
            active = [],
            css_classes = ["cluster_checkbox_label"]
        )
        cluster_checkbox.on_change('active', lambda attr, old, new: self.show_select())
        widgets_dict = {'cluster_checkbox' : cluster_checkbox}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict

    
    """
    follwing are callback functions
    """
    def update_var(self):
        """
        callback of choose_map  
        change select list of x, y axis 
        update self.plot_source by coordinates 
        """
        self.init_coordinates()
        self.update_plot_source_by_coords()
        self.plot_coordinates()
        self.update_layout()

    def update_axis(self, widget_key, attr, old, new):
        """
        switch axis and update visualized stuff of this tab
        """
        self.widgets_dict[widget_key].value = new
        self.update_plot_source_by_coords()
        self.plot_coordinates()
        self.update_layout()
    
    def update_log(self, attr, old, new):
        """
        switch axis and update visualized stuff of this tab
        """
        if self.widgets_dict['is_log'].active == [0, 1]:
            if old == [0]:
                self.widgets_dict['is_log'].active = [1]
            else:
                self.widgets_dict['is_log'].active = [0]
        self.update_plot_source_by_coords()
        self.plot_coordinates()
        self.update_layout()
    
    def create_group_select(self,
        group_name: str | None = None
    ):
        """
        update group_select widget  
        first update uns according to group_name and group_select   
        next update group_select    
        then update cluster_checkbox    
        finally visualize by uns
        """
        group_list = self.widgets_dict['group_select'].options
        if not group_name:
            group_name = self.widgets_dict['group_name'].value        
            if group_name == '':
                print("Reject: name should not be empty")
                return
            elif group_name == 'Please create a group':
                print("Reject: name conflict, 'Please create a group' is reserved")
                return
            elif group_name in group_list:
                print("Reject: name already exists")
                return
            self.widgets_dict['group_name'].value = ''
        if group_name not in dt.adata.uns['group_dict']:
            dt.init_uns(dt.adata, group_name, default = False)     
        self.init_group_select(group_name)
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()

    def rename_group_select(self):
        """
        rename current group      
        first reject illegal operations according to group_name and group_select    
        next update uns and obs    
        then update group_select    
        finally visualize
        """
        group_list = self.widgets_dict['group_select'].options
        group_name = self.widgets_dict['group_select'].value
        new_name = self.widgets_dict['group_name'].value
        if group_name != 'Please create a group':
            if  new_name == 'Please create a group':
                print("Reject: name conflict")
                return
            elif new_name == '':
                print("Reject: group name shouldn't be empty")
                return
            elif new_name in group_list:
                print("Reject: name already exists")
                return
        else: 
            print("Please create a group first")
            return
        dt.adata.obs.rename(columns = {group_name: new_name}, inplace=True)
        dt.adata.uns['group_dict'][new_name] = dt.adata.uns['group_dict'].pop(group_name)
        self.init_group_select(new_name)
        self.update_layout()

    def delete_group_select(self):
        """
        delete current group      
        first delete corresponding column/df in obs and uns    
        next update group_select    
        then update cluster_select    
        finally update self.plot_source and visualize
        """
        group_list = self.widgets_dict['group_select'].options
        group_name = self.widgets_dict['group_select'].value
        if group_name in group_list:
            group_list.remove(group_name)
            del dt.adata.obs[group_name]
            del dt.adata.uns['group_dict'][group_name]
        if group_list == []:
            group_list = ['Please create a group']
        self.init_group_select(group_list[0])
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()

    def update_group(self):
        """
        update cluster_checkbox 
        first update cluster_ckeckbox according to group_select and uns   
        then update colors according to uns  
        finally visualize
        """
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()

    def create_cluster_select(self):
        """
        add a cluster to cluster_checkbox
        if no group is created, create a group in adata.obs, adata.uns first
        next for all cases, update obs, uns with new cluster name
        then init cluster_checkbox and update colors according to uns
        finally visualize
        """
        curgroup = self.widgets_dict['group_select'].value
        curclsname = self.widgets_dict['cluster_name'].value
        self.widgets_dict['cluster_name'].value = ''
        curcolor = self.widgets_dict['color_picker'].color
        selected_list = self.figure.source.selected.indices
        if curgroup == 'Please create a group':
            group_name = self.widgets_dict['group_name'].value
            if group_name == '':
                curgroup = self.widgets_dict['x_varname'].value + '+' + self.widgets_dict['y_varname'].value
            elif group_name == 'Please create a group':
                print("Reject: name conflict, 'Please create a group' is reserved")
                return
            elif group_name in self.widgets_dict['group_select'].options:
                print("Reject: name already exists")
                return
            else:
                curgroup = group_name
                self.widgets_dict['group_name'].value = ''
            dt.init_uns(dt.adata, curgroup, default = False)
            self.init_group_select(curgroup)
        clusterlist = dt.adata.uns['group_dict'][curgroup].index.tolist()
        if curclsname == '':
            print("Reject: empty cluster name is not allowed")
            return
        elif curclsname in clusterlist:
            print("Reject: cluster name already existed")
            return
        for i in selected_list:
            curindex = dt.adata.obs.index[i]
            dt.adata.obs.loc[curindex, curgroup] = curclsname
            dt.adata.obs.loc[curindex, 'color'] = curcolor
        dt.adata.uns['group_dict'][curgroup].loc[curclsname] = [curcolor, 0]
        dt.update_uns_by_obs(dt.adata, curgroup)
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()
    
    def rename_cluster_select(self):
        """
        rename a certain cluster    
        first judge whether cluster and name input are correct  
        then update cluster name in obs and uns 
        finally init cluster_checkbox and visualize
        """
        active_cls = self.widgets_dict['cluster_checkbox'].active
        if len(active_cls) > 2:
            print("Reject: multiple clusters with the same name is not allowed")
            return
        curgroup = self.widgets_dict['group_select'].value
        clusterlist = dt.adata.uns['group_dict'][curgroup].index.to_list()
        clusterlist_active = [clusterlist[i] for i in active_cls if i < len(clusterlist)]
        if 'unassigned' in clusterlist_active:
            print("Warning: 'unassigned' can't be renamed")
            clusterlist_active.remove('unassigned')
        if len(clusterlist_active) == 2:
            print("Reject: multiple clusters with the same name is not allowed")
            return
        elif len(clusterlist_active) == 0:
            print("Warning: No cluster renamed")
            return
        cluster_name_old =  clusterlist[active_cls[0]]
        cluster_name_new = self.widgets_dict['cluster_name'].value
        self.widgets_dict['cluster_name'].value = ''
        if cluster_name_new == 'unassigned':
            print("Reject: default cluster name 'unassigned' is reserved")
            return
        elif cluster_name_new in clusterlist:
            print("Reject: new cluster name already exists")
            return
        elif cluster_name_new == '':
            print("Reject: empty cluster name not allowed")
            return
        dt.adata.obs[curgroup] = dt.adata.obs[curgroup].replace(cluster_name_old, cluster_name_new)   
        dt.adata.uns['group_dict'][curgroup].loc[cluster_name_new] = dt.adata.uns['group_dict'][curgroup].loc[cluster_name_old]
        dt.adata.uns['group_dict'][curgroup] = dt.adata.uns['group_dict'][curgroup].drop(cluster_name_old, axis = 0)
        self.init_cluster_select()
        self.update_layout()

    def delete_cluster_select(self):
        """
        delete cluster selected (merge them into 'unassigned')  
        first prepocess with clusters selected by leaving out 'unassigned' and examine length   
        next update obs, uns    
        then init cluster_checkbox  
        finally update self.plot_source by color and visualize
        """
        active_cls = self.widgets_dict['cluster_checkbox'].active
        if 0 in active_cls:
            print("Warning: default cluster 'unassigned' won't be deleted")
            active_cls.remove(0)
        if len(active_cls) == 0:
            print("Warning: No cluster deleted")
            return
        curgroup = self.widgets_dict['group_select'].value
        clusterlist = dt.adata.uns['group_dict'][curgroup].index.to_list()
        clusterlist_active = [clusterlist[i] for i in active_cls if i < len(clusterlist)]
        dt.adata.obs.loc[dt.adata.obs[curgroup].isin(clusterlist_active), curgroup] = 'unassigned'
        dt.adata.uns['group_dict'][curgroup].drop(clusterlist_active, inplace = True)
        dt.update_uns_by_obs(dt.adata, curgroup)
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()

    def merge_cluster_select(self):
        """
        merge selected clusters 
        first deal with targe name and colors   
        next deal with clusters to delete
        then update obs and uns 
        finally update clusterlist, self.plot_source and visualize
        """
        active_cls = self.widgets_dict['cluster_checkbox'].active
        if len(active_cls) <= 1:
            print("Warning: at least 2 cluster should be choosed")
            return
        curclsname = self.widgets_dict['cluster_name'].value
        self.widgets_dict['cluster_name'].value = ''
        curgroup = self.widgets_dict['group_select'].value
        clusterlist = dt.adata.uns['group_dict'][curgroup].index.to_list()
        clusterlist_active = [clusterlist[i] for i in active_cls if i < len(clusterlist)]
        curcolor = self.widgets_dict['color_picker'].color
        exist_color = dt.adata.uns['group_dict'][curgroup]['color'].tolist()
        active_color = [exist_color[i] for i in active_cls if i < len(exist_color)]
        if 'unassigned' in clusterlist_active:
            curclsname = 'unassigned'
            curcolor = dt.adata.uns['group_dict'][curgroup].loc['unassigned', 'color']
            print("Warning: merge into 'unassigned', namely delete other clusters selected")
        elif curclsname == '':
            curclsname = clusterlist_active[0]
            print("Warning: no cluster name input, take first selected cluster as default")
        elif (curclsname in clusterlist) and (curclsname not in clusterlist_active):
            curclsname = clusterlist_active[0]
            print("Warning: name already exist, take first selected cluster name as default")
        if curclsname in clusterlist_active:
            clusterlist_active.remove(curclsname)
        if (curcolor in exist_color) and (curcolor not in active_color):
            curcolor = active_color[0]
            print("Warning: color selected, take first selected cluster color as default")
        dt.adata.obs.loc[dt.adata.obs[curgroup].isin(clusterlist_active), curgroup] = curclsname
        dt.adata.obs.loc[dt.adata.obs[curgroup].isin(clusterlist_active), 'color'] = curcolor
        dt.adata.uns['group_dict'][curgroup].loc[curclsname] = {'color': curcolor}
        dt.adata.uns['group_dict'][curgroup].drop(clusterlist_active, inplace = True)
        dt.update_uns_by_obs(dt.adata, curgroup)
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()

    def add_to(self):
        """
        add chosen points to the seleced cluster  
        first make sure one and only one cluster is chosen   
        then update obs and uns 
        finally update clusterlist, self.plot_source and visualize
        """
        selected_list = self.figure.source.selected.indices
        if not selected_list:
            print("Warning: no point selected")
            return
        active_cls = self.widgets_dict['cluster_checkbox'].active
        if not active_cls:
            print("Warning: no cluster selected")
            return
        elif len(active_cls) > 1:
            print("Reject: a point can't be in multiple clusters in the same group")
            return
        curgroup = self.widgets_dict['group_select'].value
        cls_name = dt.adata.uns['group_dict'][curgroup].index.tolist()
        active_cls_name = cls_name[active_cls[0]]
        cell_list = dt.adata.obs.index.tolist()
        for i in selected_list:
            dt.adata.obs.loc[cell_list[i], curgroup] = active_cls_name
        dt.update_uns_by_obs(dt.adata, curgroup)
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()

    def remove_from(self):
        """
        remove chosen points from the seleced cluster  
        first make sure points and clusters are chosen   
        then update obs and uns 
        finally update clusterlist, self.plot_source and visualize
        """
        selected_list = self.figure.source.selected.indices
        if not selected_list:
            print("Warning: no point selected")
            return
        active_cls = self.widgets_dict['cluster_checkbox'].active
        if not active_cls:
            print("Warning: no cluster selected")
            return
        curgroup = self.widgets_dict['group_select'].value
        cls_name = dt.adata.uns['group_dict'][curgroup].index.tolist()
        active_cls_name = [cls_name[i] for i in active_cls]
        if active_cls_name == ['unassigned']:
            print("Warning: can't be removed from 'unassigned'")
            return
        cell_list = dt.adata.obs.index.tolist()
        for i in selected_list:
            if dt.adata.obs.loc[cell_list[i], curgroup] in active_cls_name:
                dt.adata.obs.loc[cell_list[i], curgroup] = 'unassigned'
        dt.update_uns_by_obs(dt.adata, curgroup)
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()

    def update(self):
        """
        update chosen points as all points of the seleced cluster  
        first make sure points and a single cluster are chosen  
        (cluster name and color won't be changed here)     
        then update obs and uns 
        finally update clusterlist, self.plot_source and visualize
        """
        selected_list = self.figure.source.selected.indices
        if not selected_list:
            print("Warning: no point selected")
            return
        active_cls = self.widgets_dict['cluster_checkbox'].active
        if not active_cls:
            print("Warning: no cluster selected")
            return
        elif len(active_cls) > 2:
            print("Reject: a point can't be in multiple clusters in the same group")
            return 
        curgroup = self.widgets_dict['group_select'].value
        cls_name = dt.adata.uns['group_dict'][curgroup].index.tolist()
        active_cls_name = [cls_name[i] for i in active_cls]
        if 'unassigned' in active_cls_name and len(active_cls) == 1:
            print("Warning: 'unassigned' can't be updated independently")
            return
        elif 'unassigned' not in active_cls_name and len(active_cls) == 2:
            print("Reject: a point can't be in multiple clusters in the same group")
            return
        elif 'unassigned' in active_cls_name and len(active_cls) == 2:
            active_cls_name.remove('unassigned')
        dt.adata.obs.loc[dt.adata.obs[curgroup].isin(active_cls_name), curgroup] = 'unassigned'
        curcolor = dt.adata.uns['group_dict'][curgroup].loc[active_cls_name[0], 'color']
        cell_list = dt.adata.obs.index.to_list()
        for i in selected_list:
            dt.adata.obs.loc[cell_list[i], curgroup] = active_cls_name[0]
            dt.adata.obs.loc[cell_list[i], 'color'] = curcolor
        dt.update_uns_by_obs(dt.adata, curgroup)
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()

    def change_cluster_color(self):
        """
        change color of selected color  
        first reject changing color of cluster 'unassigned' and give warnings of same color       
        then update obs and uns 
        finally update clusterlist, self.plot_source and visualize
        """
        curcolor = self.widgets_dict['color_picker'].color
        curgroup = self.widgets_dict['group_select'].value
        active_cls = self.widgets_dict['cluster_checkbox'].active
        cls_name = dt.adata.uns['group_dict'][curgroup].index.tolist()
        active_name = [cls_name[i] for i in active_cls]
        if 'unassigned' in active_name:
            print("Warning: color of 'unassigned' cluster won't be changed")
            active_name.remove('unassigned')
        if len(active_name) == 0:
            print("Warning: no cluster other than 'unassigned' is selected")
            return
        elif len(active_name) > 1:
            print("Warning: 2 or more clusters will be given the same color")
        exist_color = dt.adata.uns['group_dict'][curgroup]['color'].tolist()
        active_color = [exist_color[i] for i in active_cls]
        if (curcolor in exist_color) and (curcolor not in active_color):
            print("Warning: color conflict with other clusters")
        for name in active_name:
            dt.adata.uns['group_dict'][curgroup].loc[name, 'color'] = curcolor
            dt.adata.obs.loc[dt.adata.obs[curgroup].isin(active_name), 'color'] = curcolor
        self.init_cluster_select()
        self.update_plot_source_by_colors()
        self.plot_coordinates()
        self.update_layout()

    def show_select(self):
        curgroup = self.widgets_dict['group_select'].value
        active_cls = self.widgets_dict['cluster_checkbox'].active
        cls_name = dt.adata.uns['group_dict'][curgroup].index.tolist()
        active_cls_name = [cls_name[i] for i in active_cls]
        selected = [
            idx for idx, cellname in enumerate(dt.adata.obs.index)
            if dt.adata.obs.at[cellname, curgroup] in active_cls_name
        ]
        self.figure.source.selected.indices = selected
        self.update_layout()
    

    """
    following are other supportive functions called above
    """
    def get_var(self):
        """
        return variables according to current map
        """
        curmap = self.widgets_dict['choose_map'].value
        if curmap == 'generic_columns':
            varlist = dt.adata.var.index.to_list()
        else:
            varlist = dt.adata.obsm[curmap].columns.tolist()
        return varlist 
    
    def get_log_status(self):
        """
        provide reference information for whether original data is log-scaled
        """
        if np.isclose(dt.adata.X, np.trunc(dt.adata.X)).all():            
            return "log info: original data probably not log-scaled"
        else:
            return "log info: original data probably log-scaled already"

    
    def get_cluster_list(self):
        """
        organize text of cluster checkbox by uns    
        return option list of cluster_checkbox
        """
        curgroup = self.widgets_dict['group_select'].value
        cluster_promtlist = []
        for cluster_name in dt.adata.uns['group_dict'][curgroup].index:
            cellnum = dt.adata.uns['group_dict'][curgroup].loc[cluster_name, 'cell_num']
            cluster_prompt = str(cluster_name) + ": cell_nums = " + str(cellnum)
            cluster_promtlist.append(cluster_prompt)
        return cluster_promtlist
    
    def update_plot_source_by_coords(self):
        """
        update self.plot_source 
        """
        choose_map = self.widgets_dict['choose_map'].value
        x_varname = self.widgets_dict['x_varname'].value
        y_varname = self.widgets_dict['y_varname'].value
        if self.widgets_dict['is_log'].active == []:
            is_log = False
            is_exp = False
        elif self.widgets_dict['is_log'].active == [0]: 
            is_log = True
            is_exp = False
        elif self.widgets_dict['is_log'].active == [1]:
            is_log = False
            is_exp = True
        if choose_map == 'generic_columns':
            if (x_varname in dt.adata.var.index.tolist()) and (y_varname in dt.adata.var.index.tolist()):
                x_index = dt.adata.var.index.get_loc(x_varname)
                y_index = dt.adata.var.index.get_loc(y_varname)
                x_list = dt.adata.X[:, x_index]
                y_list = dt.adata.X[:, y_index]    
            else: 
                print("Fatal: 'generic_columns' Plot.__get_source: variable not exist")
                return None
        elif choose_map in dt.adata.obsm_keys():
            varnames = dt.adata.obsm[choose_map].columns.tolist()
            if (x_varname in varnames) and (y_varname in varnames):
                x_list = dt.adata.obsm [choose_map] [x_varname].tolist()
                y_list = dt.adata.obsm [choose_map] [y_varname].tolist()
            else: 
                print("Fatal: 'keys' Plot.__get_source: variable not exist")
                return None
        if is_log:
            x_list = np.log1p(x_list)
            y_list = np.log1p(y_list)
        if is_exp:
            x_list = np.expm1(x_list)
            y_list = np.expm1(y_list)
        self.plot_source['x'].clear()
        self.plot_source['y'].clear()
        self.plot_source['x'][x_varname] = x_list
        self.plot_source['y'][y_varname] = y_list
    
    def update_plot_source_by_colors(self):
        curgroup = self.widgets_dict['group_select'].value
        for cell_name in dt.adata.obs.index:
            cell_type = dt.adata.obs.loc[cell_name, curgroup]
            dt.adata.obs.loc[cell_name, 'color'] = dt.adata.uns['group_dict'][curgroup].loc[cell_type, 'color']
        self.plot_source['color'] = dt.adata.obs['color'].to_list() 

    def plot_coordinates(self,
        selected : list | None = None
    ):
        """
        update self.figure by self.plot_source
        """
        source = ColumnDataSource(
            data = {
                list(self.plot_source['x'].keys())[0] : list(self.plot_source['x'].values())[0],
                list(self.plot_source['y'].keys())[0] : list(self.plot_source['y'].values())[0],
                'color': self.plot_source['color']
            }
        )
        if selected:
            source.selected.indices = selected
        plot_dict = {'source' : source}
        self.figure.update_source(**plot_dict)
    
    def update_layout(self):
        """
        modify current tab and visualize
        """
        coords_key = ['choose_map', 'x_varname', 'y_varname', 'is_log', 'log_info'] 
        values = [self.widgets_dict[key] for key in coords_key if key in self.widgets_dict]
        layout_coords = column(values)

        group_key = ['group_name', 'create_group', 'rename_group', 'delete_group', 'group_select']
        values = [self.widgets_dict[key] for key in group_key if key in self.widgets_dict]
        layout_group = column(values)

        color_key = ['color_picker']
        values = [self.widgets_dict[key] for key in color_key if key in self.widgets_dict]
        layout_color = column(values)

        cluster_key = ['cluster_name', 'create_cluster', 'rename_cluster', 'delete_cluster', 'merge_cluster',
            'add_to', 'remove_from', 'update', 'change_cluster_color', 'cluster_checkbox']
        values = [self.widgets_dict[key] for key in cluster_key if key in self.widgets_dict]
        layout_cluster = column(values)

        self.layout = row([self.figure.plot, row([column([layout_coords, layout_color]), layout_group, layout_cluster])])
        tb.curpanel = self.name
        tb.view_panel(tb.panel_dict, tb.ext_layout, tb.curpanel)