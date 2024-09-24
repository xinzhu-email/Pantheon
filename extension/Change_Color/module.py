import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))
from bokeh.models import Select, Button, CheckboxGroup, TextInput, ColorPicker, AutocompleteInput, ColumnDataSource
from bokeh.palettes import d3
from bokeh.layouts import row, column
from Pantheon.scpantheon.myplot import Plot
import data as dt
import tabs as tb
import numpy as np
import pandas as pd

class Widgets_Color:
    
    def __init__(self,
        name: str,
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
        self.update_data()
        self.widgets_dict = dict()
        self.figure = Plot()
        self.layout = None
        self.init_map()
        self.init_coordinates()
        self.init_group()
        self.init_color()
        self.init_cluster()
        self.plot_coordinates()
        self.update_layout()


    def update_data(self):
        my_obsm = np.zeros((dt.adata.n_obs, 2))
        dt.adata.obsm['cluster'] = my_obsm
        if dt.adata.obsm:
            for key in dt.adata.obsm_keys(): 
                if type(dt.adata.obsm[key]) == np.ndarray:
                    column_names = list([key + str(i) for i in range(dt.adata.obsm[key].shape[1])])
                    dt.adata.obsm[key] = pd.DataFrame(
                        dt.adata.obsm[key],
                        index = dt.adata.obs_names,
                        columns = column_names
                    )

    def init_map(self):
        """
        a new map is automatically created when a new function is called  
        the derived data of observations in different dimensions is stored in an obsm  
        this functions creates the choose_map widget with obsm_keys
        """
        map_list = dt.adata.obsm_keys() + ['generic_columns'] 
        choose_map = Select(
            title = 'Choose map:',
            value = map_list[0],
            options = map_list
        )
        choose_map.on_change('value',lambda attr, old, new :self.update_var())
        widgets_dict = {'choose_map' : choose_map}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
        dt.adata.uns[choose_map.value] = dict()
    
    def init_coordinates(self):
        x_axis = AutocompleteInput(
            title = "x axis:", 
            value = self.get_var()[0], 
            completions = self.get_var(), 
            min_characters = 1
        )
        x_axis.on_change("value", lambda attr, old, new : self.update_axis('x_varname', attr, old, new))

        y_axis = AutocompleteInput(
            title = "y axis:", 
            value = self.get_var()[1], 
            completions = self.get_var(), 
            min_characters = 1
        )
        y_axis.on_change("value", lambda attr, old, new : self.update_axis('y_varname', attr, old, new))

        log_axis = CheckboxGroup (labels = ['Log-scaled axis'], active = [])
        log_axis.on_change('active',lambda attr, old, new: self.update_log(attr, old, new))

        widgets_dict = {'x_varname' : x_axis, 'y_varname' : y_axis, 'is_log' : log_axis}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict

    def init_group(self):      
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
        self.init_group_select()
    
    def init_group_select(self,
        grouplist: list | None = ['Please create a group'],
        update_cluster: bool | None = True    
    ):
        self.widgets_dict['group_name'].value = '' 
        group_select = Select(
            title='Select Cluster Group:',
            options = grouplist,
            value = grouplist[-1]
        )
        group_select.on_change("value", lambda attr, old, new : self.update_group())
        widgets_dict = {'group_select' : group_select}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
        if update_cluster:
            self.update_group()
  
    def init_color(self):
        color_selection = ColorPicker(
            title = "Select color:",
            color = dt.color_list[0], 
            css_classes = dt.color_list
        )
        color_change = Button(label = 'Color Change')
        color_change.on_click (lambda : self.change_color())
        widgets_dict = {'color_selection' : color_selection, 'color_change' : color_change}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
    
    def init_cluster(self):
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
        self.init_cluster_select()

    def init_cluster_select(self,
    ):
        clusterlist = ['Unassigned: color = grey, cell_nums = ' + str(dt.adata.n_obs)]

        class_checkbox = CheckboxGroup(
            labels = clusterlist,
            active = [],
            css_classes = ["class_checkbox_label"]
        )
        class_checkbox.on_change('active', lambda attr, old, new: self.show_select())
        widgets_dict = {'class_checkbox' : class_checkbox}
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
        self.update_group()
    
    def update_cluster_select(self,
        clusterlist: list | None = None,
    ):
        """
        When group selection is changed, update cluster list
        """
        if clusterlist == None:
            clusterlist = ['Unassigned: color = grey, cell_nums = ' + str(dt.adata.n_obs)]
        self.widgets_dict['class_checkbox'].labels = clusterlist
        self.widgets_dict['class_checkbox'].active = []

    
    def create_cluster_select (self):
        curmap = self.widgets_dict['choose_map'].value
        curgroup = self.widgets_dict['group_select'].value
        curclsname = self.widgets_dict['cluster_name'].value
        self.widgets_dict['cluster_name'].value = ''
        curcolor = self.widgets_dict['color_selection'].color
        selected_list = self.figure.source.selected.indices
        if curgroup == 'Please create a group':
            group_name = self.widgets_dict['x_varname'].value + '+' + self.widgets_dict['y_varname'].value
            curgroup = group_name
            index = [curclsname, 'unassigned']
            columns = ['cell_num', 'color']
            group_unsdf = pd.DataFrame(index = index, columns = columns)
            group_unsdf.loc['unassigned', 'color'] = dt.color_list[0]
            group_unsdf.loc[curclsname, 'color'] = curcolor
            group_unsdf.loc['unassigned', 'cell_num'] = dt.adata.n_obs - len(selected_list)
            group_unsdf.loc[curclsname, 'cell_num'] = len(selected_list)
            dt.adata.uns[curmap][curgroup] = group_unsdf
            dt.adata.obs[curgroup] = 'unassigned'
            for i in selected_list:
                curindex = dt.adata.obs.index[i]
                dt.adata.obs.loc[curindex, curgroup] = curclsname
                dt.adata.obs.loc[curindex, 'color'] = curcolor
            self.create_group_select(group_name)    
        clusterlist = dt.adata.uns[curmap][curgroup].index.tolist()
        if curclsname == '':
            print("Reject: empty cluster name is not allowed")
            return
        elif curclsname in clusterlist:
            print("Reject: cluster name already existed")
            return
        # change obs
        for i in selected_list:
            curindex = dt.adata.obs.index[i]
            dt.adata.obs.loc[curindex, curgroup] = curclsname
            dt.adata.obs.loc[curindex, 'color'] = curcolor
        # change uns
        new_cls = {'cell_num': len(selected_list), 'color': curcolor}
        dt.adata.uns[curmap][curgroup].loc[curclsname] = new_cls
        self.update_cluster_list()   

    def rename_cluster_select (self):
        active_cls = self.widgets_dict['class_checkbox'].active
        if len(active_cls) != 1:
            print("Reject: one and only one cluster can be renamed at a time")
            self.widgets_dict['cluster_name'].value = ''
            return
        else:
            curmap = self.widgets_dict['choose_map'].value 
            curgroup = self.widgets_dict['group_select'].value
            curclsname = self.widgets_dict['cluster_name'].value
            self.widgets_dict['cluster_name'].value = ''
            clusterlist = dt.adata.uns[curmap][curgroup].index.tolist()
            cluster_name =  clusterlist[active_cls[0]]
            if cluster_name == 'unassigned':
                print("Reject: default cluster 'unassigned' can't be renamed")
                return
            elif curclsname in clusterlist:
                print("Reject: new cluster name already exists")
                return
            elif curclsname == '':
                print("Reject: empty cluster name not allowed")
                return
            else:
                dt.adata.obs[curgroup] = dt.adata.obs[curgroup].replace(cluster_name, curclsname)
                newunsdf = dt.adata.uns[curmap][curgroup].index.map(
                    lambda x: curclsname if x == cluster_name else x
                )
                dt.adata.uns[curmap][curgroup].index = newunsdf
                self.update_cluster_list()

    def delete_cluster_select (self):
        active_cls = self.widgets_dict['class_checkbox'].active
        total_cls = len(self.widgets_dict['class_checkbox'].labels)
        if len(active_cls) == 0:
            print("Warning: no cluster selected")
            return
        elif active_cls[-1] == total_cls - 1:
            print("Warning: default cluster 'unassigned' won't be deleted")
            if len(active_cls) == 1:
                return
            del active_cls[-1]
        curmap = self.widgets_dict['choose_map'].value 
        curgroup = self.widgets_dict['group_select'].value
        cluster_name = [dt.adata.uns[curmap][curgroup].index.tolist()[i] for i in active_cls]
        dt.adata.obs.loc[dt.adata.obs[curgroup].isin(cluster_name), 'color'] = dt.color_list[0]
        dt.adata.obs.loc[dt.adata.obs[curgroup].isin(cluster_name), curgroup] = 'unassigned'
        # ensure the clustername and color is right in the list, cell_num will be updated in update_cluster_list
        dt.adata.uns[curmap][curgroup].drop(cluster_name, inplace = True)
        self.update_cluster_list()

    def merge_cluster_select(self):
        active_cls = self.widgets_dict['class_checkbox'].active
        if len(active_cls) <= 1:
            print("Warning: at least 2 cluster should be choosed")
            return
        else:
            curclsname = self.widgets_dict['cluster_name'].value
            self.widgets_dict['cluster_name'].value = ''
            curmap = self.widgets_dict['choose_map'].value
            curgroup = self.widgets_dict['group_select'].value
            cls_name = dt.adata.uns[curmap][curgroup].index.tolist()
            active_cls_name = [cls_name[i] for i in active_cls]
            curcolor = self.widgets_dict['color_selection'].color
            exist_color = dt.adata.uns[curmap][curgroup]['color'].tolist()
            active_color = [exist_color[i] for i in active_cls]
            if 'unassigned' in active_cls_name:
                curclsname = 'unassigned'
                curcolor = dt.adata.uns[curmap][curgroup].loc['unassigned', 'color']
                print("Warning: merge into 'unassigned' means delete the clusters selected")
            else:
                if curclsname == '':
                    curclsname = active_cls_name[0]
                    print("Warning: no cluster name input, take first selected cluster as default")
                elif (curclsname in cls_name) and (curclsname not in active_cls_name):
                    curclsname = active_cls_name[0]
                    print("Warning: name already exist, take first selected cluster name as default")
                if (curcolor in exist_color) and (curcolor not in active_color):
                    curcolor = active_color[0]
                    print("Warning: color selected, take first selected cluster color as default")
            dt.adata.obs.loc[dt.adata.obs[curgroup].isin(active_cls_name), curgroup] = curclsname
            dt.adata.obs.loc[dt.adata.obs[curgroup].isin(active_cls_name), 'color'] = curcolor
            dt.adata.uns[curmap][curgroup].drop(active_cls_name, inplace = True)
            cell_num_tot = dt.adata.uns[curmap][curgroup].loc[
                dt.adata.uns[curmap][curgroup].index.isin(active_cls_name), 'cell_num'
            ].sum()
            new_cls = {'cell_num': cell_num_tot, 'color': curcolor}
            dt.adata.uns[curmap][curgroup].loc[curclsname] = new_cls
            self.update_cluster_list()
    
    def add_to(self):
        selected_list = self.figure.source.selected.indices
        if not selected_list:
            print("Warning: no point selected")
            return
        active_cls = self.widgets_dict['class_checkbox'].active
        if not active_cls:
            print("Warning: no cluster selected")
            return
        elif len(active_cls) > 1:
            print("Reject: a point can't be in multiple clusters in the same group")
            return
        curmap = self.widgets_dict['choose_map'].value
        curgroup = self.widgets_dict['group_select'].value
        cls_name = dt.adata.uns[curmap][curgroup].index.tolist()
        active_cls_name = cls_name[active_cls[0]]
        cellnames = dt.adata.obs.index.tolist()
        for i in selected_list:
            dt.adata.obs.loc[cellnames[i], curgroup] = active_cls_name
        self.update_cluster_list()
    
    def remove_from(self):
        selected_list = self.figure.source.selected.indices
        if not selected_list:
            print("Warning: no point selected")
            return
        active_cls = self.widgets_dict['class_checkbox'].active
        if not active_cls:
            print("Warning: no cluster selected")
            return
        curmap = self.widgets_dict['choose_map'].value
        curgroup = self.widgets_dict['group_select'].value
        cls_name = dt.adata.uns[curmap][curgroup].index.tolist()
        active_cls_name = [cls_name[i] for i in active_cls]
        if active_cls_name == ['unassigned']:
            print("Warning: can't be removed from 'unassigened'")
            return
        cellnames = dt.adata.obs.index.tolist()
        for i in selected_list:
            if dt.adata.obs.loc[cellnames[i], curgroup] in active_cls_name:
                dt.adata.obs.loc[cellnames[i], curgroup] = 'unassigned'
        self.update_cluster_list()
    
    def update(self):
        selected_list = self.figure.source.selected.indices
        if not selected_list:
            print("Warning: no point selected")
            return
        active_cls = self.widgets_dict['class_checkbox'].active
        if not active_cls:
            print("Warning: no cluster selected")
            return
        elif len(active_cls) > 2:
            print("Reject: a point can't be in multiple clusters in the same group")
            return 
        else:
            curmap = self.widgets_dict['choose_map'].value
            curgroup = self.widgets_dict['group_select'].value
            curcolor = self.widgets_dict['color_selection'].color
            cls_name = dt.adata.uns[curmap][curgroup].index.tolist()
            active_cls_name = [cls_name[i] for i in active_cls]
            if 'unassigned' in active_cls_name and len(active_cls) == 1:
                print("Warning: 'unassigened' can't be updated independently")
                return
            elif 'unassigned' not in active_cls_name and len(active_cls) == 2:
                print("Reject: a point can't be in multiple clusters in the same group")
                return
            elif 'unassigned' in active_cls_name and len(active_cls) == 2:
                active_cls_name.remove('unassigned')
            dt.adata.obs.loc[dt.adata.obs[curgroup].isin(active_cls_name), curgroup] = 'unassigned'
            cellnames = dt.adata.obs.index.to_list()
            for i in selected_list:
                dt.adata.obs.loc[cellnames[i], curgroup] = active_cls_name[0]
                dt.adata.obs.loc[cellnames[i], 'color'] = curcolor
            dt.adata.uns[curmap][curgroup].loc[active_cls_name[0], 'color'] = curcolor
            self.update_cluster_list()
    
    def show_select(self):
        curmap = self.widgets_dict['choose_map'].value
        curgroup = self.widgets_dict['group_select'].value
        active_cls = self.widgets_dict['class_checkbox'].active
        cls_name = dt.adata.uns[curmap][curgroup].index.tolist()
        active_cls_name = [cls_name[i] for i in active_cls]
        selected = []
        for cellname in dt.adata.obs.index.to_list():
            if dt.adata.obs.loc[cellname, curgroup] in active_cls_name:
                cellindex = dt.adata.obs.index.get_loc(cellname)
                selected.append(cellindex)
        self.plot_coordinates(selected)
        self.update_layout()        
    
    def update_cluster_list(self):
        curmap = self.widgets_dict['choose_map'].value
        curgroup = self.widgets_dict['group_select'].value
        cluster_numdict = dt.adata.obs[curgroup].value_counts().to_dict()
        color_dict = dt.adata.uns[curmap][curgroup]['color'].to_dict()
        combined_dict = dict() 
        for key in color_dict:
            if key in cluster_numdict:
                combined_dict[key] = (cluster_numdict[key], color_dict[key])
            else:
                combined_dict[key] = (0, color_dict[key])
        unassigned_num = combined_dict['unassigned'][0]
        del combined_dict['unassigned']
        combined_dict['unassigned'] = (unassigned_num, color_dict['unassigned'])
        newunsdf = pd.DataFrame(
            list(combined_dict.values()), 
            columns = ['cell_num', 'color'], 
            index = list(combined_dict.keys())
        )      
        dt.adata.uns[curmap][curgroup] = newunsdf
        # update checkbox list
        clusterlist = []
        for clustername in dt.adata.uns[curmap][curgroup].index:
            curcellnum = dt.adata.uns[curmap][curgroup].loc[clustername, 'cell_num']
            cluster = clustername + ': cell_nums = ' + str(curcellnum)
            clusterlist.append(cluster)
        self.widgets_dict['cluster_name'].value = ''
        self.update_cluster_select(clusterlist)
        self.plot_coordinates()
        self.update_layout()
    
    def change_cluster_color(self):
        curcolor = self.widgets_dict['color_selection'].color
        curmap = self.widgets_dict['choose_map'].value
        curgroup = self.widgets_dict['group_select'].value
        active_cls = self.widgets_dict['class_checkbox'].active
        cls_name = dt.adata.uns[curmap][curgroup].index.tolist()
        active_name = [cls_name[i] for i in active_cls]
        if 'unassigned' in active_name:
            print("Warning: color of 'unassigned' cluster won't be changed")
            active_name.remove('unassigned')
        if len(active_name) == 0:
            print("Warning: no cluster other than 'unassigned' is selected")
            return
        elif len(active_name) > 1:
            print("Warning: 2 or more clusters will be given the same color")
        exist_color = dt.adata.uns[curmap][curgroup]['color'].tolist()
        active_color = [exist_color[i] for i in active_cls]
        if (curcolor in exist_color) and (curcolor not in active_color):
            print("Warning: color conflict with other clusters")
        for name in active_name:
            dt.adata.uns[curmap][curgroup].loc[name, 'color'] = curcolor
            dt.adata.obs.loc[dt.adata.obs[curgroup].isin(active_name), 'color'] = curcolor
        self.plot_coordinates()
        self.update_layout()        

    def update_group(self):
        curmap = self.widgets_dict['choose_map'].value
        curgroup = self.widgets_dict['group_select'].value
        if curgroup == 'Please create a group':
            dt.adata.obs['color'] = dt.adata.obs['default']
            if 'class_checkbox' in self.widgets_dict:
                self.update_cluster_select()
                self.plot_coordinates()
                self.update_layout()
            return
        else:
            if curgroup not in dt.adata.uns[curmap]:
                index = ['unassigned']
                columns = ['cell_num', 'color']
                group_unsdf = pd.DataFrame(index = index, columns = columns)
                group_unsdf.loc['unassigned', 'color'] = dt.color_list[0]
                group_unsdf.loc['unassigned', 'cell_num'] = dt.adata.n_obs
                dt.adata.uns[curmap][curgroup] = group_unsdf
                dt.adata.obs[curgroup] = 'unassigned'

            for cell_name in dt.adata.obs.index:
                cell_type = dt.adata.obs.loc[cell_name, curgroup]
                dt.adata.obs.loc[cell_name, 'color'] = dt.adata.uns[curmap][curgroup].loc[cell_type, 'color']
            clusterlist = []
            for clustername in dt.adata.uns[curmap][curgroup].index:
                curcellnum = dt.adata.uns[curmap][curgroup].loc[clustername, 'cell_num']
                cluster = clustername + ': cell_nums = ' + str(curcellnum)
                clusterlist.append(cluster)
            self.widgets_dict['cluster_name'].value = ''
            self.update_cluster_select(clusterlist)
            self.plot_coordinates()
            self.update_layout()
              
    
    def get_var(self):
        map_name = self.widgets_dict['choose_map'].value
        if map_name == 'generic_columns':
            varlist = dt.adata.var.index.to_list()
        else:
            varlist = dt.adata.obsm[map_name].columns.tolist()
        return varlist
    
    def update_var(self):
        self.init_coordinates()
        self.plot_coordinates()
        self.update_layout()
    
    def update_axis(self, widget_key, attr, old, new):
        self.widgets_dict[widget_key].value = new
        self.plot_coordinates()
        self.update_layout()
    
    def update_log(self, attr, old, new):
        self.plot_coordinates()
        self.update_layout()
    
    def create_group_select(self,
        group_name: str | None = None
    ):
        if 'group_select' in self.widgets_dict:
            group_list = self.widgets_dict['group_select'].options
            if group_name == None:
                group_name = self.widgets_dict['group_name'].value
            if group_name == '':
                print("Reject: name should not be empty")
                return group_list
            elif group_name == 'Please create a group':
                print("Reject: name conflict")
                return group_list
            elif group_name in group_list:
                print("Reject: name already exists")
                return group_list
            else: 
                if 'Please create a group' in group_list:
                    group_list.remove('Please create a group')
                group_list.append(group_name)                
        else: 
            group_list = ['Please create a group']
        self.init_group_select(group_list)
    
    def rename_group_select(self):
        group_list = self.widgets_dict['group_select'].options
        group_name = self.widgets_dict['group_select'].value
        new_name = self.widgets_dict['group_name'].value
        curmap = self.widgets_dict['choose_map'].value
        if group_name != 'Please create a group':
            if  new_name == 'Please create a group':
                print("Reject: name conflict")
                return group_list 
            elif new_name == '':
                print("Reject: group name shouldn't be empty")
                return group_list
            elif new_name in group_list:
                print("Reject: name already exists")
                return group_list
            else:
                for i in range(len(group_list)):
                    if group_list[i] == group_name:
                        group_list[i] = new_name
        else: 
            print("Please create a group first")
        self.init_group_select(group_list, update_cluster = False)
        dt.adata.obs.rename(columns={group_name: new_name}, inplace=True)
        dt.adata.uns[curmap][new_name] = dt.adata.uns[curmap].pop(group_name)
        self.plot_coordinates()
        self.update_layout()
    
    def delete_group_select(self):
        group_list = self.widgets_dict['group_select'].options
        group_name = self.widgets_dict['group_select'].value
        curmap = self.widgets_dict['choose_map'].value
        if group_name in group_list:
            group_list.remove(group_name)
            del dt.adata.obs[group_name]
            del dt.adata.uns[curmap][group_name]
        if group_list == []:
            group_list = ['Please create a group']
        self.init_group_select(group_list)
    
    def change_color(self):
        curcolor = self.widgets_dict['color_selection'].color
        curmap = self.widgets_dict['choose_map'].value
        curgroup = self.widgets_dict['group_select'].value
        if curgroup not in dt.adata.uns[curmap]:
            for i in self.figure.source.selected.indices:
                curindex = dt.adata.obs.index[i]
                dt.adata.obs.loc[curindex, 'color'] = curcolor
            self.plot_coordinates()
            self.update_layout()          
        else:
            print("Reject: pointweise color change isn't allowed, try 'cluster color'")
            return        
    
    def get_params(self):
        choose_map = self.widgets_dict['choose_map'].value
        x_varname = self.widgets_dict['x_varname'].value
        y_varname = self.widgets_dict['y_varname'].value
        if self.widgets_dict['is_log'].active == []:
            is_log = False
        else: 
            is_log = True

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
        curmap = self.widgets_dict['choose_map'].value
        curgroup = self.widgets_dict['group_select'].value
        if curgroup in dt.adata.uns[curmap]:
            for cell_name in dt.adata.obs.index:
                cell_type = dt.adata.obs.loc[cell_name, curgroup]
                dt.adata.obs.loc[cell_name, 'color'] = dt.adata.uns[curmap][curgroup].loc[cell_type, 'color']
        else:
            dt.adata.obs['color'] = dt.adata.obs['default']
        color = dt.adata.obs['color'].to_list()
        source = ColumnDataSource (data = {x_varname : x_list, y_varname : y_list, 'color' : color})
        plot_dict = {'source' : source}
        return plot_dict
    
    def plot_coordinates(self,
        selected : list | None = None
    ):
        plot_dict = self.get_params()
        if selected:
            plot_dict['selected'] = selected 
        self.figure.update_source(**plot_dict)
    
    def update_layout(self):

        coords_key = ['choose_map', 'x_varname', 'y_varname', 'is_log'] 
        values = [self.widgets_dict[key] for key in coords_key if key in self.widgets_dict]
        layout_coords = column(values)

        group_key = ['group_name', 'create_group', 'rename_group', 'delete_group', 'group_select']
        values = [self.widgets_dict[key] for key in group_key if key in self.widgets_dict]
        layout_group = column(values)

        color_key = ['color_selection', 'color_change']
        values = [self.widgets_dict[key] for key in color_key if key in self.widgets_dict]
        layout_color = column(values)

        cluster_key = ['cluster_name', 'create_cluster', 'rename_cluster', 'delete_cluster', 'merge_cluster',
            'add_to', 'remove_from', 'update', 'change_cluster_color', 'class_checkbox']
        values = [self.widgets_dict[key] for key in cluster_key if key in self.widgets_dict]
        layout_cluster = column(values)

        self.layout = row([self.figure.plot, row([column([layout_coords, layout_color]), layout_group, layout_cluster])])
        tb.curpanel = self.name
        tb.view_panel(tb.panel_dict, tb.ext_layout, tb.curpanel)
