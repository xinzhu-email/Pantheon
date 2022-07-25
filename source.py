
import json
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, CustomJS, Circle, Div, Panel, Tabs, CheckboxGroup, FileInput,FixedTicker, ColorBar, LogColorMapper
from bokeh.models.widgets import Select, Button, ColorPicker,TextInput, DataTable, MultiSelect, AutocompleteInput
from bokeh.events import ButtonClick
from bokeh.transform import linear_cmap, log_cmap
from bokeh.palettes import d3
from bokeh.layouts import row, column, layout
from bokeh.io import curdoc
from bokeh.layouts import row
from bokeh.plotting import figure
import pandas
import numpy as np
import anndata
import scipy.sparse as ss
import colorcet as cc
import scanpy as sc
# from main3 import change_class_color
from transform import data_trans
import os, sys





TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
        ("color", "@color"),
]
class FlowPlot:
    def __init__(self, data=None, color_map=None, x_init_idx = 0, y_init_idx = 0, allow_select = True, select_color_change = True, legend = None, main_plot = None,title=None):
        self.adata = data
        self.data_df = self.adata.to_df()
        self.data_log = np.log1p(self.data_df)     
        self.label_existed, view_existed = False, False
        try:
            group_list = list(self.adata.uns['category_dict'].keys())
            if main_plot == None:
                self.label_existed = True
        except:
            self.adata.uns['category_dict'] = dict() 
        self.adata.obs['ind'] = pandas.Series(np.array(range(self.data_df.shape[0])).astype(int).tolist(), index=self.data_df.index)  
        self.data_columns = self.data_df.columns.values.tolist()
        self.data_df['color'] = pandas.Series(d3['Category20c'][20][0], index=self.data_df.index)
        self.data_log['color'] = pandas.Series(d3['Category20c'][20][0], index=self.data_df.index)
        self.data_df['hl_gene'] = pandas.Series(np.full(self.data_df.shape[0], 3), index=self.data_df.index)                         
        self.opts = dict(plot_width=500, plot_height=500, min_border=0, tools="pan,lasso_select,box_select,wheel_zoom,save")
        views = list(self.adata.obsm.keys())
        if views != []:
            for view_name in views:
                for i in range(self.adata.obsm[view_name].shape[1]):
                    self.data_df[view_name+str(i)] = pandas.Series(self.adata.obsm[view_name][:,i],index=self.data_df.index)
                    self.data_log[view_name+str(i)] = self.data_df[view_name+str(i)]
            view_existed = True
        else:
            view_existed = False
        self.source = ColumnDataSource(data=self.data_df)
        self.view = CDSView(source=self.source, filters=[IndexFilter([i for i in range(self.data_df.shape[0])])])
        self.cur_color = color_list[0]
        self.p = figure(width=500, height=500, tools="pan,lasso_select,box_select,tap,wheel_zoom,save,hover",title=title, tooltips=TOOLTIPS)
        #self.p.output_backend = "svg"
        #print("backend is ", self.p.output_backend)        
        if view_existed:
            view_list = list(self.adata.obsm.keys())+['generic_columns']
            self.choose_panel = Select(title='Choose map:',value=view_list[0],options=view_list)
            self.data_columns = list([self.choose_panel.value +str(i) for i in range(self.adata.obsm[self.choose_panel.value].shape[1])])
        else:
            self.choose_panel = Select(title='Choose map:',value='generic_columns',options=['generic_columns'])
        self.choose_panel.on_change('value',lambda attr, old, new :self.change_view_list())
        self.p.xaxis.axis_label = self.data_columns[x_init_idx]
        self.p.yaxis.axis_label = self.data_columns[y_init_idx]
        self.r = self.p.circle(self.data_columns[x_init_idx], self.data_columns[y_init_idx],  source=self.source, view=self.view, fill_alpha=1,fill_color=color_map,line_color=None )
        self.p.legend.click_policy="hide"
        self.s_x = AutocompleteInput(title="x:", value=self.data_columns[x_init_idx], completions=self.data_columns, min_characters=1)
        self.s_y = AutocompleteInput(title="y:", value=self.data_columns[y_init_idx], completions=self.data_columns, min_characters=1)
        # Attach reaction
        self.s_x.on_change("value", lambda attr, old, new: tag_func(self.s_x, self.r.glyph, 'x', self.p) )
        self.s_y.on_change("value", lambda attr, old, new: tag_func(self.s_y, self.r.glyph, 'y', self.p) )
        # Set default fill color
        if select_color_change:
            self.r.selection_glyph = Circle(fill_alpha=1,fill_color=self.cur_color, line_color='black')
        self.allow_select = allow_select
        print('label and view existed',self.label_existed,view_existed)

        ######################################
        ####### Create panels of plots #######
        ######################################    

        # Show gene list
        self.show_gene_list = Div(text='Gene/Marker List: '+str(self.data_columns[0:10]))
        # Log
        self.log_axis = CheckboxGroup(labels=['Log-scaled axis'],active=[])
        self.log_axis.on_change('active',lambda attr, old, new: self.log_cb())
        # Change the color of selected parts
        self.color_selection = ColorPicker(title="Select color:", color=color_list[0], css_classes=color_list)
        self.color_selection.on_change("color", lambda attr,old,new: self.select_color_func())
        # Gate, remove, and show all button
        self.gate_button = Button(label="Gate")
        self.gate_button.on_click(self.gate_func)
        self.remove_button = Button(label="Trim")
        self.remove_button.on_click(self.remove_func)
        self.showall_button = Button(label="Show All")
        self.showall_button.on_click(self.showall_func)

        ### Class Group Functions Buttons ###
        # Select class group
        if self.label_existed:
            group_list = list(self.adata.uns['category_dict'].keys())
            self.group = Select(title='Select Cluster Group:', options=group_list, value=group_list[-1])
            # self.update_checkbox()
            # self.show_color()
        else:
            self.group = Select(title='Select Cluster Group:',options=[' '],value=' ')
        self.group.on_change('value', lambda attr, old, new: self.choose_cat())
        # Input name of new category
        self.group_name = TextInput(title='Input Group Name: ', value='')
        self.group_name.js_on_change("value", CustomJS(code="""
            console.log('text_input: value=' + this.value, this.toString())
        """))
        # Create New Category
        self.create_group = Button(label='Create Group')
        self.create_group.on_click(self.new_category)
        # Rename Category
        self.rename_group = Button(label='Rename Group')
        self.rename_group.on_click(self.edit_category)
        # Delete Category
        self.delete_group = Button(label='Delete Group')
        self.delete_group.on_click(self.del_category)

        ###### Class Function Buttons #######
        # Select of class (use checkbox)
        cls_label = ['Unassigned: color=grey, cell_nums=' + str(self.data_df.shape[0])] # Checkbox label of class
        self.class_checkbox = CheckboxGroup(labels=cls_label, active=[], css_classes=["class_checkbox_label"])
        self.class_checkbox.on_change('labels',lambda attr, old, new: self.text_color())
        self.class_checkbox.on_change('active',lambda attr, old, new: self.text_color())
        # Show Selected classes on plot
        self.show_selected_class = Button(label='Select Cluster')
        self.show_selected_class.on_click(self.show_checked)
        # Show color on checkbox
        self.checkbox_color = Button(label='Show Color on Checkbox')
        self.checkbox_color.on_click(self.text_color)
        # Paragraph to store color
        self.para_color = Div(text='0', visible=False, css_classes=['hide'])
        # Div to trigger change on js
        self.trigger_color = Div(text='1', visible=False)
        self.trigger_color.js_on_change('text',CustomJS(code="""
            
            setTimeout(function(){
                const collection = document.getElementsByClassName("class_checkbox_label");
                var str = document.getElementsByClassName('hide')[0].children[0].innerHTML;
                console.log(document.getElementsByClassName('hide')[0].children[0].innerHTML);
                const color = str.split(' ');
                var k = color.length;
                console.log(k,color);
                for (var i=0;i<k;i++)
                {
                    collection[0].children[0].children[i].style.color = color[i];
                }
                console.log('collection:' + collection[0].children[0].innerHTML);
            }, 500);
            
            
        """))
        # Input of class name
        self.class_name = TextInput(title='Input Cluster Name: ', value='')
        # Create New Class
        self.new_class = Button(label='Create Cluster')
        self.new_class.on_click(self.add_entry)      
        # Merge Button
        self.merge_class = Button(label='Merge Cluster')
        self.merge_class.on_click(self.merge)
        # Rename cluster
        self.rename_class = Button(label='Rename Cluster')
        self.rename_class.on_click(self.rename)
        # Delete cluster
        self.delete_class = Button(label='Delete Cluster')
        self.delete_class.on_click(self.del_class) 
        # Add dots button
        self.add_to = Button(label='Add to')
        self.add_to.on_click(self.save_cls_button)
        # Remove dots from cluster
        self.remove_from = Button(label='Remove from')
        self.remove_from.on_click(self.remove_dot)
        # Update cluster
        self.update_class = Button(label='Update Cluster')
        self.update_class.on_click(self.update_clus)
        # Change Color
        self.change_class_color = Button(label='Change Color')
        self.change_class_color.on_click(self.change_color)
        if self.label_existed:
            self.update_checkbox()
            self.show_color()


        ###### Highlight Gene #######
        if main_plot != None:
            self.hl_bar_map = LogColorMapper(palette=cc.kbc[::-1], low=1, high=20)
            hl_color_bar = ColorBar(color_mapper=self.hl_bar_map, label_standoff=8, border_line_color=None)
            self.p.add_layout(hl_color_bar,'right')
            self.hl_input = AutocompleteInput(completions=list(self.adata.var.index), title="Select Highlight Gene: ", min_characters=1)
            # Show Highlight Gene
            self.hl_button = Button(label="Show Highlight Gene")
            self.hl_button.on_click(self.show_colorbar)
            # Filt cells according to gene expression
            self.hl_filt = Select(options=['Gene Expression >','Gene Expression =','Gene Expression <'],value='Gene Expression >')
            self.hl_filt_num = TextInput()
            self.hl_filt_button = Button(label='Filter')
            self.hl_filt_button.on_click(self.hl_filter)
            # Comfirm to change the selected dots in main view
            self.hl_comfirm = Button(label='Change Selected')
            self.hl_comfirm.on_click(lambda event: self.change_select(main_plot))




    def refresh(self):
        self.r.selection_glyph.fill_color = self.cur_color
    
    ##################################
    ####### Call Back Functions ######
    ##################################
    # Change view list
    def change_view_list(self):
        if self.choose_panel.value != 'generic_columns':
            column_list = list([self.choose_panel.value + str(i) for i in range(self.adata.obsm[self.choose_panel.value].shape[1])])
        else:
            column_list = list(self.adata.var.index)
        self.s_x.completions = column_list
        self.s_y.completions = column_list
        print(column_list)

    # Log
    def log_cb(self):
        if self.log_axis.active == []:
            self.data_df['color'] = self.source.data['color']
            self.data_df['hl_gene'] = self.source.data['hl_gene']
            self.source.data = self.data_df
            print(self.log_axis.active)
        else:
            self.data_log['color'] = self.source.data['color']
            self.data_log['hl_gene'] = self.source.data['hl_gene']
            self.source.data = self.data_log
            print(self.log_axis.active)

    # Callback of colorpicker(selection), update the selected dots with picked color
    def select_color_func(self):
        self.cur_color = self.color_selection.color
        self.r.selection_glyph.fill_color = self.cur_color
        # Just to trigger plot update 
        self.source.data["color"] = self.source.data["color"]
        print('now color',self.r.selection_glyph.fill_color)

    # Show all, gate, and remove function
    def gate_func(self):
        if len(self.view.filters) != 0:
            indices = list(set(self.source.selected.indices)&set(self.view.filters[0].indices))
        else:
            indices = self.source.selected.indices
        self.view.filters = [IndexFilter(indices)]

    def remove_func(self):
        if len(self.view.filters) == 0:
            self.view.filters = [IndexFilter(np.object_(range(self.data_df.shape[0])))]
        remain_indices = [x for x in self.view.filters[0].indices if x not in self.source.selected.indices]
        self.view.filters = [IndexFilter(remain_indices)]

    def showall_func(self):
        self.view.filters = list([])

    # Show the saved color of dots
    def correct_func(self):
        self.source.selected.indices = []


    # Select class group
    def choose_cat(self):
        try: 
            self.adata.uns['category_dict'][self.group.value]['class_name'][0]
            self.update_checkbox()
            print(self.adata.uns['category_dict'][self.group.value])
            self.class_checkbox.active = [0]
            self.show_color()
        except:
            self.class_checkbox.labels = ['Unassigned: color=grey, cell_nums=' + str(self.data_df.shape[0])]
            self.class_checkbox.active = []
        #self.text_color()

    # New Category
    def new_category(self):
        if self.group_name.value == '':
            marker = str(self.p.xaxis.axis_label) + '+' + str(self.p.yaxis.axis_label)
        else:
            marker = self.group_name.value
        self.adata.uns['category_dict'][marker] = pandas.DataFrame(columns=['class_name','color','cell_num'])
        self.adata.obs[marker] = pandas.Series(index=self.data_df.index,dtype=object)
        self.group.options = list(self.adata.uns['category_dict'].keys())
        self.group.value = marker
        self.group_name.value = ''
        #print('new group',self.group.value, marker,self.group.options, '=')

    # Edit category
    def edit_category(self):   
        old_name = self.group.value
        new_name = self.group_name.value
        self.adata.obs[new_name] = self.adata.obs.pop(old_name)
        self.adata.uns['category_dict'][new_name] = self.adata.uns['category_dict'].pop(old_name)
        self.group.options = list(self.adata.uns['category_dict'].keys())
        self.group.value = new_name
        print(self.adata.uns['category_dict'])

    # Delete category
    def del_category(self):
        del self.adata.uns['category_dict'][self.group.value]   
        del self.adata.obs[self.group.value]
        self.group.options = list(self.adata.uns['category_dict'].keys())
        if len(self.group.options) == 0:
            self.group.value = ''
        else:
            self.group.value = self.group.options[0]


    #### Class Callback Function #####
    # Update the label of class checkbox
    def update_checkbox(self):
        cate = self.group.value
        cls_label = []
        num = 0
        for i in range(self.adata.uns['category_dict'][cate].shape[0]):
            class_name = self.adata.uns['category_dict'][cate]['class_name'][i]
            cell_num = len(self.data_df[self.adata.obs[cate]==str(i)])       
            s = str(class_name) +  ': cell_nums=' + str(cell_num)
            cls_label = np.append(cls_label,s)
            num = num + cell_num
        cls_label = np.append(cls_label,str('Unassigned: color=grey, cell_nums=' + str(self.data_df.shape[0]-num))) 
        self.class_checkbox.labels = list(cls_label)
        #self.text_color()

    def show_checked(self):
        #source.selected.indices = temp[temp[cat_opt.value]==str(self.class_checkbox.active[0])].index
        self.source.selected.indices = list(self.adata.obs[self.adata.obs[self.group.value].isin(list(str(i) for i in self.class_checkbox.active))]['ind'])
        self.show_color()

    # Show color on checkbox
    def text_color(self):
        color_js = ''
        try:
            length = len(self.adata.uns['category_dict'][self.group.value]['color']) 
            for i in range(length):
                color_js = color_js + self.adata.uns['category_dict'][self.group.value]['color'][i] + ' '
            self.para_color.text = color_js + color_list[18]
        except:
            length = 1
            #color_js = [color_list[18]]
            self.para_color.text = str(color_list[18])
        self.trigger_color.text = self.trigger_color.text + '1'
        #print('CALL',color_js)


    # Save change of classes
    def save_class(self, cate, class_name, color, n):
        if n == 0:
            ind = len(self.class_checkbox.labels)-1
        else:
            ind = self.class_checkbox.active[0]  
        class_label = list(self.adata.obs[cate])
        #print('ind=====',ind)
        for i in self.source.selected.indices:
            class_label[i] = str(ind)
            #print('i:',i)
        self.adata.obs[cate] = class_label
        #print(class_label)
        cate = self.group.value
        self.update_checkbox()
        self.class_checkbox.active = [ind]
        self.show_color()
        self.correct_func()
        #self.text_color()

    # New Class
    def add_entry(self):
        xaxis = str(self.p.xaxis.axis_label)
        yaxis = str(self.p.yaxis.axis_label)
        #if str(cat_opt.value) != xaxis+'+'+yaxis and str(cat_opt.value) != yaxis+'+'+xaxis:
        if self.group.value == ' ':
            print(str(self.group.value),xaxis+'+'+yaxis)
            #self.class_checkbox.labels = ['no cluster: color=' + color_list[18] + ', cell_nums=' + str(self.data_df.shape[0])]
            self.new_category()       
        cell_num = len(self.source.selected.indices)
        print('add cluster',self.group.value)
        self.adata.uns['category_dict'][self.group.value].loc[len(self.adata.uns['category_dict'][self.group.value])] = {'class_name':self.class_name.value,'color':self.cur_color,'cell_num':cell_num}
        self.save_class(self.group.value, self.class_name.value, self.cur_color, 0)
        self.class_name.value = ''
        

    # Merge checked classes
    def merge(self):
        group = self.group.value
        if self.class_name.value == '':
            toclass = self.adata.uns['category_dict'][group]['class_name'][self.class_checkbox.active[0]]
            color = self.adata.uns['category_dict'][group]['color'][self.class_checkbox.active[0]]
        else:
            toclass = self.class_name.value
            color = self.cur_color

        self.adata.uns['category_dict'][group].drop(index=self.class_checkbox.active,inplace=True)
        temp = pandas.DataFrame(self.adata.uns['category_dict'][group],columns=['class_name','color','cell_num'],index=self.adata.uns['category_dict'][group].index)
        temp['new'] = pandas.Series(range(temp.shape[0]),index=temp.index)
        count = 0
        clr = self.source.data['color']
        for i in range(self.data_df.shape[0]):
            ind  = str(self.adata.obs[group][i])
            old = True
            for j in range(len(self.class_checkbox.active)):
                if self.adata.obs[group][i] == str(self.class_checkbox.active[j]):
                    old = False
                    clr[i] = color
                    self.adata.obs[group][i] = str(len(temp))
                    count = count + 1
                    break
            if old:
                try:
                    self.adata.obs[group][i] = str(temp[temp.index == int(ind)].loc['new'])
                except:
                    count = count
        
        self.adata.uns['category_dict'][group] = pandas.DataFrame(self.adata.uns['category_dict'][group],index=temp['new'])
        print('----',self.adata.uns['category_dict'][group])
        self.adata.uns['category_dict'][group].loc[len(temp)] = {'class_name':toclass,'color':color,'cell_num':count}
        del_list2 = self.class_checkbox.labels
        for i in range(len(self.class_checkbox.active)):
            del del_list2[self.class_checkbox.active[i]-i]
        tt = del_list2[-1]
        del_list2[-1] = str(toclass+ ': cell_nums='+ str(count))
        del_list2 = del_list2 + [tt]
        self.class_checkbox.labels = del_list2
        self.class_checkbox.active = []
        self.source.data['color'] = clr
        #self.text_color()

    # Delete Class
    def del_class(self):
        group = self.group.value
        self.adata.uns['category_dict'][group].drop(index=self.class_checkbox.active,inplace=True)
        temp = pandas.DataFrame(self.adata.uns['category_dict'][group],columns=['class_name','color','cell_num'],index=self.adata.uns['category_dict'][group].index)
        temp['new'] = pandas.Series(range(temp.shape[0]),index=temp.index)
        count = 0
        clr = self.source.data['color']
        print(clr)
        for i in range(self.data_df.shape[0]):
            ind  = str(self.adata.obs[group][i])
            old = True
            for j in range(len(self.class_checkbox.active)):
                if self.adata.obs[group][i] == str(self.class_checkbox.active[j]):
                    old = False
                    clr[i] = color_list[18]
                    self.adata.obs[group][i] = np.nan
                    count  = count + 1
                    break
            if old: 
                try:
                    self.adata.obs[group][i] = str(temp[temp.index == int(ind)].loc['new'])
                except:
                    count = count + 1
        del_list2 = self.class_checkbox.labels
        for i in range(len(self.class_checkbox.active)):
            del del_list2[self.class_checkbox.active[i]-i]
        del_list2[-1] = str('unassigned: color=grey, cell_nums=' + str(count))
        self.class_checkbox.labels = del_list2
        self.class_checkbox.active = []
        self.adata.uns['category_dict'][group] = pandas.DataFrame(self.adata.uns['category_dict'][group],index=temp['new'])
        self.source.data['color'] = clr
        #self.text_color()

    # Rename class
    def rename(self):
        ind = self.class_checkbox.active[0]
        print('rename ind:',ind)
        cell_num = self.adata.uns['category_dict'][self.group.value]['cell_num'][ind]

        labels = self.class_checkbox.labels
        labels[ind] = str(self.class_name.value) + ': cell_nums=' + str(cell_num)
        self.adata.uns['category_dict'][self.group.value]['class_name'][ind] = self.class_name.value
        self.class_name.value = ''
        print(labels)
        self.class_checkbox.labels = labels
        #self.text_color()

    # Add dots to cluster
    def save_cls_button(self):
        class_name = self.adata.uns['category_dict'][self.group.value]['class_name'][self.class_checkbox.active[0]]
        color = self.adata.uns['category_dict'][self.group.value]['color'][self.class_checkbox.active[0]]
        cell_num = len(self.source.selected.indices)
        self.save_class(self.group.value, class_name, color, cell_num)
        print(self.adata.uns['category_dict'][self.group.value])

    # Remove dots from cluster
    def remove_dot(self):
        cl_label = self.adata.obs[self.group.value]
        for i in self.source.selected.indices:
            for j in self.class_checkbox.active:
                if cl_label[i] == str(j):
                    cl_label[i] = np.NAN
                    break
        self.adata.obs[self.group.value] = cl_label
        self.update_checkbox()
        self.show_color()

    # Update class
    def update_clus(self):
        ind = self.class_checkbox.active[0]
        #adata.obs[adata.obs[cat_opt.value]==str(ind)].loc[cat_opt.value] = pandas.Series(index=[0],dtype=object)[0]
        cl_label = self.adata.obs[self.group.value]
        cl_label[self.adata.obs[self.group.value]==str(ind)] = np.NAN
        print(cl_label)
        for i in self.source.selected.indices:
            cl_label[i] = str(ind)
        self.adata.obs[self.group.value] = cl_label
        self.update_checkbox()
        self.show_color()
        #self.text_color()

    # change color of class
    def change_color(self):
        color_l = self.source.data['color']
        self.show_checked()
        for i in self.source.selected.indices:
            color_l[i] = self.cur_color
        self.source.data['color'] = color_l
        self.adata.uns['category_dict'][self.group.value]['color'][[i for i in self.class_checkbox.active]] = self.cur_color
        self.text_color()
        #print(hide.value,now_color)

    #### Highly variable gene functions #####
    def show_colorbar(self):
        updated_color = self.source.data[self.hl_input.value]
        updated_color = (updated_color-min(updated_color))*(self.hl_bar_map.high - self.hl_bar_map.low)/(max(updated_color)-min(updated_color))
        self.source.data["hl_gene"] = updated_color
    
    def hl_filter(self):
        try:
            index_list = list(self.view.filters.indices)
        except:
            index_list = list(self.view.filters[0].indices)
        if self.hl_filt.value == 'Gene Expression >':
            index_list = list(self.adata.obs[self.source.data[self.hl_input.value] > float(self.hl_filt_num.value)]['ind'])
        elif self.hl_filt.value == 'Gene Expression <':
            index_list = list(self.adata.obs[self.source.data[self.hl_input.value] < float(self.hl_filt_num.value)]['ind'])
        else:
            index_list = list(self.adata.obs[self.source.data[self.hl_input.value] == float(self.hl_filt_num.value)]['ind'])
        index_list = set(index_list)&set(list(self.view.filters[0].indices))
        self.source.selected.indices = list(index_list)
        #new_r = show_colorbar()
        self.r.selection_glyph = Circle(fill_alpha=1,fill_color='Black')
        #print(self.source.selected.indices)

    def change_select(self, main_plot):
        main_plot.source.selected.indices = self.source.selected.indices

    def change_view(self,main_plot):
        self.r.glyph.x = main_plot.r.glyph.x
        self.r.glyph.y = main_plot.r.glyph.y
        self.p.xaxis.axis_label = main_plot.p.xaxis.axis_label
        self.p.yaxis.axis_label = main_plot.p.yaxis.axis_label
        self.view.filters = main_plot.view.filters

    #### Other Functions ####
    # Show color of category
    def show_color(self):
        #global source
        col_list = self.source.data['color']
        #print(adata.obs[cat_opt.value])
        for i in range(self.data_df.shape[0]):
            ind = self.adata.obs[self.group.value][i]
            #print(ind)
            try:
                ind = int(ind)
                col_list[i] = self.adata.uns['category_dict'][self.group.value]['color'][ind]
            except:
                col_list[i] = color_list[18]
        self.source.data['color'] = col_list





class CreateTool:
    
    def __init__(self,adata):
        self.adata = adata
        self.hl_gene_map = log_cmap('hl_gene', cc.kbc[::-1], low=1, high=20)

    def set_function(self, effector, attr, value):
        setattr(effector, attr, value)
        

    def base_tool(self):        
        Figure = FlowPlot(data=self.adata, color_map='color',title='Main Plot')
        module_checkbox = CheckboxGroup(labels=load_options(),active=[],name='modules_checkbox')
        #module_buttons = CheckboxGroup(labels=[], name='module_buttons')
        #select_module = Select(title='Select Module:', options=['Change color'], value='Change Color')
        #import_button = Button(label='Import Module')
        #import_button.on_click(lambda: load_package(list(module_checkbox.active)))
        layout=row(column(Figure.p, Figure.show_gene_list, Figure.para_color, Figure.trigger_color, module_checkbox),
            column(Figure.choose_panel,Figure.s_x, Figure.s_y, Figure.log_axis, Figure.color_selection, Figure.gate_button, Figure.remove_button, Figure.showall_button),
            column(Figure.group, Figure.group_name, Figure.create_group, Figure.rename_group, Figure.delete_group,
             Figure.class_name, Figure.new_class, Figure.checkbox_color, Figure.class_checkbox),
            column(Figure.show_selected_class, Figure.add_to, Figure.remove_from, Figure.update_class, 
             Figure.rename_class,  Figure.merge_class, Figure.delete_class))
        module_checkbox.on_change('active', lambda attr, old, new: load_package(list(module_checkbox.active), layout))    
        return Figure, layout
    
    def highlight_gene(self, main_plot):
        hl_figure = FlowPlot(data=self.adata, color_map=self.hl_gene_map, main_plot=main_plot,title='Highlight Gene Plot')
        layout = row(hl_figure.p,column(hl_figure.hl_input, hl_figure.hl_button, 
            row(hl_figure.hl_filt, hl_figure.hl_filt_num),hl_figure.hl_filt_button,hl_figure.hl_comfirm))
        return hl_figure, layout

    def multi_panel(self, plot_list, panel_list, title_list, update_view=False):
        tab_list = []
        for i in range(len(panel_list)):
            panel = Panel(child=panel_list[i], title=title_list[i])
            tab_list = tab_list + [panel]
        tabs = Tabs(tabs = tab_list)
        if update_view == True:
            tabs.on_change('active',lambda attr, old, new: plot_list[1].change_view(plot_list[0]))
        return tabs
    
    def trans_to_json(self, Figure):
        to_json = data_trans(Figure.adata)
        to_json = json.dumps(obj=to_json.__dict__,ensure_ascii=False)
        return to_json

        
color_list = d3['Category20c'][20]
Main_plot = FlowPlot

class connection:
    def __init__(self):
        self.Figure = Main_plot
    
    def get_attributes(self):
        if self.Figure.view.filters == []:
            remain_cells = list(range(self.Figure.data_df.shape[0]))
        else:
            remain_cells = list(self.Figure.view.filters[0].indices)
        to_json = data_trans(self.Figure.p.xaxis.axis_label, 
                             list(self.Figure.source.data['color']), 
                             self.Figure.color_selection.color,
                             list(self.Figure.class_checkbox.active),
                             self.Figure.group.value,
                             list(self.Figure.source.selected.indices),
                             remain_cells)
        to_json = json.dumps(obj=to_json.__dict__,ensure_ascii=False)
        return to_json

    def set_attributes(self,d):
        self.Figure.source.data['color'] = list(d['data_color'])
        self.Figure.view.filters = [IndexFilter(d['showing_indices'])]
        print(len(self.Figure.view.filters[0].indices))
    
    def get_anndata(self):
        adata = self.Figure.adata.copy()
        return adata
    
    def get_group_dict(self):
        return self.Figure.adata.uns['category_dict']
    
    def set_group_dict(self, group_dict):
        self.Figure.adata.uns['category_dict'] = group_dict
    
    def get_group_label(self):
        return self.Figure.adata.obs
    
    def set_group_label(self, group_label):
        self.Figure.adata.obs = group_label

class plot_function:
    def __init__(self):
        self.Figure = Main_plot
    
    def show_checked(self):
        self.Figure.show_checked()

    def change_checkbox_color(self):
        self.Figure.text_color()



def tag_func(selector, effector, attr, plot):
    axis = getattr(plot, attr + "axis")
    axis.axis_label = selector.value
    setattr(effector, attr, selector.value)

def load_options():
    try:
        options = new_layout().options()
    except:
        sys.path = [os.path.dirname(os.path.abspath(__file__))] + sys.path
        from new_func import new_layout
        options = new_layout().options()
    return options

def load_package(active, layout):    
    buttons = curdoc().get_model_by_name('module_buttons')
    try:
        curdoc().remove_root(buttons)
    except:
        print('##### NO MODULE #####')
    try:
        options = new_layout().add()
    except:
        sys.path = [os.path.dirname(os.path.abspath(__file__))] + sys.path
        from new_func import new_layout
        options = new_layout().add()

    #     print(len(options)-i-1)
    #     curdoc().remove_root(options[len(options)-i-1])
    # for i in active:
    #     curdoc().add_root(options[i])
    layouts = column()
    for i in range(len(options)):
        if i in active:
            layouts = column(layouts, options[i])
    buttons = layouts
    buttons.name = 'module_buttons'
    curdoc().add_root(buttons)
    # checkbox = curdoc().get_model_by_name('modules_checkbox')
    # print(checkbox)
    # layout.remove(checkbox)
    # layout.append(column(checkbox, layouts))
    # try:
    #     #layout.children.clear()
    #     layout.children.append(layouts)
    # except:
    #     layout.children.append(layouts)
        #curdoc().add_root(layouts)


def upload_callback(upload_button):
    global Main_plot
    loading_remind = Div(text='Loading data……')
    curdoc().add_root(loading_remind)
    try:
        adata = anndata.read_csv(upload_button.filename)
        print('csv')
    except:
        adata = anndata.read(upload_button.filename)
        print('h5ad')
    print(upload_button.filename)
    mainplot, panel1 = CreateTool(adata=adata).base_tool()
    Main_plot = mainplot
    hl_figure, panel2 = CreateTool(adata=adata).highlight_gene(mainplot)
    tab = CreateTool(adata).multi_panel([mainplot,hl_figure],[panel1,panel2], ['Main View', 'Highlight Gene'], update_view=True)
    curdoc().add_root(tab)
    curdoc().remove_root(loading_remind)


def main():
    upload_button = FileInput()
    upload_button.on_change('filename',lambda attr, old, new: upload_callback(upload_button))
    curdoc().add_root(upload_button)
    



if __name__ == "main":
    main()
