import json
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, CustomJS, Circle, Div, Panel, Tabs, CheckboxGroup, FileInput,FixedTicker, ColorBar, LogColorMapper, Widget, Quad
from bokeh.models.widgets import Select, Button, ColorPicker,TextInput, DataTable, MultiSelect, AutocompleteInput
from bokeh.events import ButtonClick
from bokeh.transform import log_cmap
from bokeh.palettes import d3
from bokeh.layouts import row, column, layout
from bokeh.io import curdoc# current document
<<<<<<< HEAD
from bokeh.plotting import figure, output_file, save, show
from bokeh.embed import components, file_html
from bokeh.resources import CDN
import pandas 
import numpy as np
import anndata
=======
from bokeh.embed import file_html
from bokeh.plotting import figure, save
from bokeh.resources import CDN
import pandas 
import numpy as np
>>>>>>> extension
import scipy.sparse as ss
import colorcet as cc
import scanpy as sc
# from new_func import new_layout
# from main3 import change_class_color
<<<<<<< HEAD

import os, sys, io
import importlib
from PyQt5.QtWidgets import *
# import mysql.connector
try: from scpantheon.front_end import save_qt
except: from front_end import save_qt
from appdirs import AppDirs
import requests, zipfile, shutil
=======
# import mysql.connector
import os, sys, io
import importlib
from PyQt5.QtWidgets import *
from appdirs import AppDirs
import requests, zipfile, tarfile, shutil, subprocess
try:
    from scpantheon.front_end import extensions_qt 
    from scpantheon.front_end.extensions_qt import get_extensions_path
    from scpantheon.front_end import save_qt, load_qt
    from scpantheon.front_end.data_qt import dir, extract_online_packages, auto_pip_install, read_path
    from scpantheon.front_end.save_qt import get_save_path
except:
    subprocess.check_call(['pip3', 'install', "scpantheon"])
    from scpantheon.front_end import extensions_qt 
    from scpantheon.front_end.extensions_qt import get_extensions_path
    from scpantheon.front_end import save_qt, load_qt
    from scpantheon.front_end.data_qt import dir, extract_online_packages, auto_pip_install, read_path
    from scpantheon.front_end.save_qt import get_save_path
>>>>>>> extension


TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
        ("color", "@color"),
]
<<<<<<< HEAD
class FlowPlot:
    global data_file
    def __init__(self, data=None, color_map=None, x_init_idx = 0, y_init_idx = 1, allow_select = True, select_color_change = True, main_plot = None,title=None): # - legend=None
        self.adata = data
        self.data_df = self.adata.to_df()
        self.data_log = np.log1p(self.data_df)    
        # For real-valued input, log1p is accurate also for x so small that 1 + x == 1 in floating-point accuracy.
        self.label_existed, view_existed = False, False
=======

class FlowPlot:
    global data_path
    def __init__(self, data=None, color_map=None, x_init_idx = 0, y_init_idx = 1, allow_select = True, select_color_change = True, main_plot = None,title=None): # - legend=None
        self.adata = data
        # !!! only plot x, y of adata
        # self.adata = self.adata[:, [x_init_idx, y_init_idx]]
        # self.adata = self.adata[:, ['CD3D','CD3E','GNLY','CD14']]
        '''print(self.adata)
        print(self.adata.var_names)'''
        self.data_df = self.adata.to_df()
        self.data_log = np.log1p(self.data_df)    
        # For real-valued input, log1p is accurate also for x so small that 1 + x == 1 in floating-point accuracy.
        self.label_existed, view_existed = False, False # group_label_existed
>>>>>>> extension
        # personalized
        try:
            group_list = list(self.adata.uns['category_dict'].keys()) 
            #  uns can get any kinds of data type like dict or list
<<<<<<< HEAD
            if main_plot == None:
                self.label_existed = True
        except:
            self.adata.uns['category_dict'] = dict()  
            # initialize the null category_dict     
            group_list = list(self.adata.obs.columns) 

            if group_list != [] and main_plot == None:
                self.label_existed = True
                for group in group_list: # every single obs
                    self.adata.uns['category_dict'][group] = pandas.DataFrame(columns=['class_name','color','cell_num']) # 2d matrix with new add columns
                                                  # key, because it's a dict
                    class_list = self.adata.obs[group] # one specific obs
                    # cell classes
                    self.adata.obs[group] = pandas.Series(self.adata.obs[group], dtype=object) # 1d ndarray with axis labels(default to RangeIndex (0, 1, 2, …, n) if not provided.)
                                                                                   ### ??? ###
                    class_dict = {}
                    for value in class_list:
                        class_dict[value] = class_dict.get(value,0) + 1 # initialize with 1 ?? ##
=======
            if main_plot == None and group_list != []:
                self.label_existed = True
        except:
            self.adata.uns['category_dict'] = dict()   
            group_list = list(self.adata.obs.columns) 
            # print("group list:", group_list)
            if group_list != [] and main_plot == None:
                self.label_existed = True
                for group in group_list: 
                    self.adata.uns['category_dict'][group] = pandas.DataFrame(columns=['class_name','color','cell_num']) 
                    class_list = self.adata.obs[group] 
                    # ??? why transform now?
                    self.adata.obs[group] = pandas.Series(self.adata.obs[group], dtype=object)
                    class_dict = {}
                    for value in class_list: # ??? every single cell value?
                        class_dict[value] = class_dict.get(value,0) + 1 
>>>>>>> extension
                    ind = 0 
                    for key in class_dict.keys():
                        self.adata.uns['category_dict'][group].loc[ind,:] = {'class_name': key, 'cell_num': class_dict[key], 'color':color_list[int(ind*4%20)]}
                        ind = ind + 1

                    
        self.adata.obs['ind'] = pandas.Series(np.array(range(self.data_df.shape[0])).astype(int).tolist(), index=self.data_df.index)  
        self.data_columns = self.data_df.columns.values.tolist()
        self.data_df['color'] = pandas.Series(d3['Category20c'][20][0], index=self.data_df.index)
        self.data_log['color'] = pandas.Series(d3['Category20c'][20][0], index=self.data_df.index)
        self.data_df['hl_gene'] = pandas.Series(np.full(self.data_df.shape[0], 3), index=self.data_df.index)    
        self.source = ColumnDataSource(data=self.data_df[self.data_columns[0:2]+['color']+['hl_gene']])                             
        self.opts = dict(plot_width=500, plot_height=500, min_border=0, tools="pan,lasso_select,box_select,wheel_zoom,save")
        views = list(self.adata.obsm.keys())
<<<<<<< HEAD
        # print('views:!!!!!!!!!!!', views)
=======
>>>>>>> extension
        if views != []:
            for view_name in views:
                for i in range(self.adata.obsm[view_name].shape[1]):
                    self.data_df[view_name+str(i)] = pandas.Series(self.adata.obsm[view_name][:,i],index=self.data_df.index)
                    self.data_log[view_name+str(i)] = self.data_df[view_name+str(i)]
            view_existed = True
        else:
            view_existed = False
        #self.source = ColumnDataSource(data=self.adata[:,0:2])
        self.view = CDSView(source=self.source, filters=[IndexFilter([i for i in range(self.data_df.shape[0])])])
        self.cur_color = color_list[0]
        self.p = figure(width=500, height=500, tools="pan,lasso_select,box_select,tap,wheel_zoom,save,hover",title=title, tooltips=TOOLTIPS, output_backend="webgl")
        #self.p.output_backend = "svg"
<<<<<<< HEAD
        #print("backend is ", self.p.output_backend)        
=======
        #print("backend is ", self.p.output_backend)     
        # Choose Map   
>>>>>>> extension
        if view_existed:
            view_list = list(self.adata.obsm.keys())+['generic_columns']
            self.choose_panel = Select(title='Choose map:', value=view_list[0], options=view_list)
            self.data_columns = list([self.choose_panel.value +str(i) for i in range(self.adata.obsm[self.choose_panel.value].shape[1])])
            self.source.data = self.data_df[self.data_columns[0:2]+['color']+['hl_gene']]
        else:
<<<<<<< HEAD

=======
>>>>>>> extension
            self.choose_panel = Select(title='Choose map:',value='generic_columns',options=['generic_columns'])
        self.choose_panel.on_change('value',lambda attr, old, new :self.change_view_list())
        self.p.xaxis.axis_label = self.data_columns[x_init_idx]
        self.p.yaxis.axis_label = self.data_columns[y_init_idx]
        self.x = x_init_idx
        self.y = y_init_idx
        # plot cell get
        self.r = self.p.circle(self.data_columns[x_init_idx], self.data_columns[y_init_idx],  source=self.source, view=self.view, fill_alpha=1,fill_color=color_map,line_color=None )
<<<<<<< HEAD

=======
>>>>>>> extension
        # glygh list
        self.glylist = [self.r,]
        self.s_x = AutocompleteInput(title="x axis:", value=self.data_columns[x_init_idx], completions=self.data_columns, min_characters=1)
        self.s_y = AutocompleteInput(title="y axis:", value=self.data_columns[y_init_idx], completions=self.data_columns, min_characters=1)
        # Attach reaction
        self.s_x.on_change("value", lambda attr, old, new: self.tag_func(self.s_x, self.r.glyph, 'x', self.p) )
        self.s_y.on_change("value", lambda attr, old, new: self.tag_func(self.s_y, self.r.glyph, 'y', self.p) )
        # Set default fill color
        if select_color_change:
            self.r.selection_glyph = Circle(fill_alpha=1,fill_color=self.cur_color, line_color='black')
        self.allow_select = allow_select
<<<<<<< HEAD
        print('label and view existed',self.label_existed,view_existed)
=======
        print('label and view existed',self.label_existed, view_existed)
>>>>>>> extension

        ######################################
        ####### Create panels of plots #######
        ######################################    
<<<<<<< HEAD
        # Input extension url
        self.extension_url = TextInput(title='Input extension url: ', value='')
=======
        # Extension url
        self.extension_url = TextInput(title='Extension url: ', value='')
>>>>>>> extension
        self.extension_url.js_on_change("value", CustomJS(code="""
            console.log('text_input: value=' + this.value, this.toString())
        """))
        # Import extension zip from online
<<<<<<< HEAD
        self.import_extension = Button(label="online extension")
        self.import_extension.on_click(self.import_func)
=======
        self.import_extension = Button(label="online extension zip")
        self.import_extension.on_click(self.load_online_extensions)
        # Extension packages
        self.extension_packages = Button(label="local extension packages")
        self.extension_packages.on_click(self.load_local_extensions)
>>>>>>> extension
        # Show gene list
        self.show_gene_list = Div(text='Gene/Marker List: '+str(self.data_columns[0:10]))
        # Show plot
        self.show_plot = Div(text="", name='Show_plot') 
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
        # Export Button
        self.export_button = Button(label='Export Results')
        self.export_button.on_click(self.save_profile)

        ### Class Group Functions Buttons ###
        # Select class group
        if self.label_existed:
<<<<<<< HEAD
            group_list = list(self.adata.uns['category_dict'].keys()) 
=======
            group_list = list(self.adata.uns['category_dict'].keys())  
>>>>>>> extension
            self.group = Select(title='Select Cluster Group:', options=group_list, value=group_list[-1])
            #self.group = Select(title='Select Cluster Group:',options=[' '],value=' ')
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
            }, 100);
            
            
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

        # Button disabled list, remember to append in each button func
        self.buttons_group = [self.gate_button,self.export_button,self.remove_button,self.showall_button,self.create_group,self.rename_group,self.delete_group,
                            self.show_selected_class,self.checkbox_color,self.new_class,self.merge_class,self.rename_class,self.delete_class,self.add_to,
<<<<<<< HEAD
                            self.remove_from,self.update_class,self.change_class_color,self.import_extension]
=======
                            self.remove_from,self.update_class,self.change_class_color,self.import_extension,self.extension_packages]
>>>>>>> extension
        self.buttons_amount = len(self.buttons_group)
        
        if self.label_existed:
            self.update_checkbox()
            self.show_color()

        ###### Highlight Gene #######
        if main_plot != None:
            self.hl_bar_map = LogColorMapper(palette=cc.kbc[::-1], low=1, high=20)
            hl_color_bar = ColorBar(color_mapper=self.hl_bar_map, label_standoff=8, border_line_color=None)
            self.p.add_layout(hl_color_bar,'right')
            self.marker_file = FileInput()
<<<<<<< HEAD
            print('++++++',self.marker_file.filename)
=======
            # print('++++++',self.marker_file.filename)
>>>>>>> extension
            self.marker_file.on_change('filename', lambda attr, old, new: self.marker_choice())
            self.cell_type = Select(title='Choose Cell Type:', options=['No cell type'], value='No cell type')
            self.cell_type.on_change('value',lambda attr, old, new: self.change_marker_ct())
            self.ct_marker = Select(title='Choose marker of the celltype', options=['Cell type not chosen'], value='Cell type not chosen')
            self.show_marker = Button(label='Show Marker Gene Expression')
            self.show_marker.on_click(lambda: self.show_colorbar(marker=True))
            self.hl_input = AutocompleteInput(completions=list(self.adata.var.index), title="Select Highlight Gene: ", min_characters=1)
            # Show Highlight Gene
            self.hl_button = Button(label="Show Highlight Gene")
            self.hl_button.on_click(lambda: self.show_colorbar(marker=False))
            # Filt cells according to gene expression
            self.hl_filt = Select(options=['Gene Expression >','Gene Expression =','Gene Expression <'],value='Gene Expression >')
            self.hl_filt_num = TextInput()
            self.hl_filt_button = Button(label='Filter')
            self.hl_filt_button.on_click(self.hl_filter)
            # Comfirm to change the selected dots in main view
            self.hl_comfirm = Button(label='Change Selected')
            self.hl_comfirm.on_click(lambda event: self.change_select(main_plot))     

    # Button disabled func
    def button_disabled(self):
        for self.b in self.buttons_group:
            self.b.disabled = True
        
 
    def button_abled(self):
        for self.b in self.buttons_group:
            self.b.disabled = False

    def refresh(self):
        self.r.selection_glyph.fill_color = self.cur_color
    
    ##################################
    ####### Call Back Functions ######
    ##################################
<<<<<<< HEAD
    # Import extension packages from online
    def import_func(self):
        self.button_disabled()
        def import_f(self):
=======
    # Import Online Extension Packages
    def load_online_extensions(self):
        global dir
        self.button_disabled()
        def load_e(self):
            global module_select_id
>>>>>>> extension
            if self.extension_url == '':
                print('please input extension url')
            else:
                zip_file_url = self.extension_url.value
            self.extension_url.value = ''
            # Download online packages and get the new extensions path
            # try :
<<<<<<< HEAD
            print('extension path:', extension_path)
            r = requests.get(zip_file_url, stream=True)
            z = zipfile.ZipFile(io.BytesIO(r.content))
            extract_path = 'C:/Users/23606/Documents/Workspace/Pantheon/online_extension_packages/' 
            '''print(os.getcwd())
            extract_path = os.getcwd() + 'online_extension_packages/'
            extract_path.replace('scpantheon')'''

            # Download online extensions packages to the extract_path
            z.extractall(extract_path)
            ''' file_names = z.namelist()
            for file_name in file_names:
                # find dir
                if file_name.endswith('/'):
                    # get dir name
                    folder_name = os.path.basename(file_name[:-1])
                    if folder_name == 'extension':
                        new_extension_path = extract_path + file_name
            print('extension from online path:', new_extension_path)'''
            
            # Find all the directory from online extension packages that has module.py
            module_path_list = []
            def find_module(path):
                lsdir = os.listdir(path)
                dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
                if dirs:
                    for i in dirs:
                        find_module(os.path.join(path, i))
                files = [i for i in lsdir if os.path.isfile(os.path.join(path,i))]
                flag = False
                for f in files:
                    if f == 'module.py':
                        flag = True
                        # module_path_list.append(os.path.join(path, f))
                if flag: 
                    module_path_list.append(path)

            find_module(extract_path)
            print('module path list:\n', module_path_list)
            # Copy all the extension module to extension path
            for module_directory in module_path_list:
                module_directory += '/'
                folder_name = os.path.basename(module_directory[:-1])
                try: 
                    shutil.copytree(module_directory, extension_path+'/'+folder_name+'/')
                    print('Module', folder_name, 'added')
                except:
                    print('Module', folder_name, 'already exists')
            print('Online packages download finished!')
            # pre_module_select = curdoc().get_model_by_name('module_select')
            # option = pre_module_select.value
            models = curdoc().get_model_by_id('1234') # pre_module_select = Select(...,id='1234') 
            # print(models)
            models.visible = False
            curdoc().remove_root(models)
            module_select = Select(title='Choose Functions to Add:', options=load_options(), value='', name='modules_select') 
            module_select.on_change('value', lambda attr, old, new: load_module(module_select.value))
            curdoc().add_root(module_select)
            '''except:
                print('please use correct extension package url')'''
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : import_f(self))
=======
            # print('extensions path:', extensions_path)
            check_code = load_qt.main()
            if check_code == 'app closed':
                extract_path = load_qt.get_load_path() + '/online_extension/'
                '''print(os.getcwd())
                extract_path = os.getcwd() + 'online_extension/'
                extract_path.replace('scpantheon')'''
                # extract online extensions package
                extract_online_packages(extensions_path, extract_path, zip_file_url)
                # load new extensions to curdoc
                load_extension_select()
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : load_e(self))
    
    # Import Local Extension Packages
    def load_local_extensions(self):
        global dir, extensions_path
        self.button_disabled()
        def load_e(self):
            global module_select_id
            check_code = extensions_qt.main()
            if check_code == 'app closed':
                extensions_path = get_extensions_path(dir) + '/'
            auto_pip_install(extensions_path)
            # load new extensions to curdoc
            load_extension_select()
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : load_e(self))
>>>>>>> extension

    # Change view list
    def change_view_list(self):
        if self.choose_panel.value != 'generic_columns':
            column_list = list([self.choose_panel.value + str(i) for i in range(self.adata.obsm[self.choose_panel.value].shape[1])])
        else:
            column_list = list(self.adata.var.index)
        self.s_x.completions = column_list
        self.s_y.completions = column_list

        print(column_list)

    # Save the anndata result
    def save_profile(self):
        global dir
        self.button_disabled()
<<<<<<< HEAD
        def next_save(self):
            if save_qt.main() == 'app closed':
                print('choosing finished')
            path = get_save_path(dir) + '/'
            text_cover(dir, path + 'result.h5ad') # write the output anndata to cover the data
            print("path covered to " + path + "result.h5ad")
            try: 
                self.adata.write_h5ad(path+'result.h5ad') 
                self.adata.obs.to_csv(path+'cluster.csv')
            except:
                os.makedirs(path)
                self.adata.write_h5ad(path+'result.h5ad') 
                self.adata.obs.to_csv(path+'cluster.csv')
            # for cate in list(self.adata.uns['category_dict'].keys()):
            #     self.adata.obs[cate].to_csv(path+'%s.csv'%cate)
            #adata.uns['category_dict']('cluster name.csv') 
=======
        def next_save(self): 
            check_code = save_qt.main()
            if check_code == 'app closed':
                # print('choosing finished')
                path = get_save_path(dir) + '/'
                text_cover(dir, path + 'result.h5ad') # write the output anndata to cover the data
                print("path covered to " + path + "result.h5ad")
                try: 
                    self.adata.write_h5ad(path+'result.h5ad') 
                    self.adata.obs.to_csv(path+'cluster.csv')
                except:
                    os.makedirs(path)
                    self.adata.write_h5ad(path+'result.h5ad')
                    self.adata.obs.to_csv(path+'cluster.csv')
                # for cate in list(self.adata.uns['category_dict'].keys()):
                #     self.adata.obs[cate].to_csv(path+'%s.csv'%cate)
                #adata.uns['category_dict']('cluster name.csv') 
>>>>>>> extension
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_save(self))

    # change x, y axis
    def tag_func(self, selector, effector, attr, plot):
        self.button_disabled()
        def tag(self, selector, effector, attr, plot):
            axis = getattr(plot, attr + "axis")
            old_name = axis.axis_label
            print('axis_label=====', axis.axis_label)
            data = pandas.DataFrame(self.source.data) 
            if plot.xaxis.axis_label != plot.yaxis.axis_label:           
                data.drop(labels=old_name, axis=1, inplace=True)
            axis.axis_label = selector.value
            if len(data) != len(self.data_df):
                if type(data['index']) == 'str':
                    data = data[data['index'].isin(list(self.adata.obs['ind']))]
                    print('int=====',data['index'],'====')
                else:
                    data = data[data['index'].isin(list(self.data_df.index))]
                    print('str=====',data['index'],'====')
            if self.log_axis.active == []:
                data.loc[:,selector.value] = pandas.Series(list(self.data_df[selector.value]), index=data.index) 
            else:
                data.loc[:,selector.value] = pandas.Series(list(self.data_log[selector.value]), index=data.index) 
            
            data.drop(labels='index', axis=1, inplace=True)
            print(data)
            self.source.data = data
            setattr(effector, attr, selector.value)
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : tag(self, selector, effector, attr, plot))

    # Log
    def log_cb(self):
        self.button_disabled()
        def log(self):
            data = pandas.DataFrame(self.source.data) 
            data.drop(labels='index', axis=1, inplace=True)
            axis_label = data.columns
            names = []
            for name in axis_label:
                if name not in ['color', 'hl_gene']:
                    names = names + [name]
                    if self.log_axis.active == []:
                        data[name] = pandas.DataFrame(list(self.data_df[name]), index=data.index) 
                    else:
                        data[name] = pandas.DataFrame(list(self.data_log[name]), index=data.index) 
            self.source.data = data
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : log(self))

    # Callback of colorpicker(selection), update the selected dots with picked color
    def select_color_func(self):
        self.button_disabled()
        def select(self):
            self.cur_color = self.color_selection.color
            self.r.selection_glyph.fill_color = self.cur_color
            # Just to trigger plot update 
            self.source.data["color"] = self.source.data["color"]
            print('now color',self.r.selection_glyph.fill_color)
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : select(self))

    # Show all, gate, and remove function
    def gate_func(self):
        self.button_disabled()
        def next_gate(self):
            if len(self.view.filters) != 0:
                indices = list(set(self.source.selected.indices)&set(self.view.filters[0].indices))
            else:
                indices = self.source.selected.indices
            self.view.filters = [IndexFilter(indices)]
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_gate(self))

    def remove_func(self):
        self.button_disabled()
        def next_remove(self):
            if len(self.view.filters) == 0:
                self.view.filters = [IndexFilter(np.object_(range(self.data_df.shape[0])))]
            remain_indices = [x for x in self.view.filters[0].indices if x not in self.source.selected.indices]
            self.view.filters = [IndexFilter(remain_indices)]
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_remove)

    def showall_func(self):
        self.button_disabled()
        def next_showall(self):
            self.view.filters = list([])
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_showall(self))

    # Show the saved color of dots
    def correct_func(self):
        self.source.selected.indices = []


    # Select class group
    def choose_cat(self):
        self.button_disabled()
        def cat(self):
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
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : cat(self))

    # New Category
    def new_category(self):
        self.button_disabled()
        def next_category(self):
            if self.group_name.value == '':
                marker = str(self.p.xaxis.axis_label) + '+' + str(self.p.yaxis.axis_label)
            else:
                marker = self.group_name.value
            self.adata.uns['category_dict'][marker] = pandas.DataFrame(columns=['class_name','color','cell_num'])
            self.adata.obs[marker] = pandas.Series(index=self.data_df.index,dtype=object)
            self.group.options = list(self.adata.uns['category_dict'].keys())
            self.group.value = marker
            print('group:', self.group.value)
            print('group_name', self.group_name.value)
            self.group_name.value = ''
            #print('new group',self.group.value, marker,self.group.options, '=')
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_category(self))

    # Rename category
    def edit_category(self):   
        self.button_disabled()
        def next_edit(self):
            old_name = self.group.value
            new_name = self.group_name.value
            self.adata.obs[new_name] = self.adata.obs.pop(old_name)
            self.adata.uns['category_dict'][new_name] = self.adata.uns['category_dict'].pop(old_name)
            self.group.options = list(self.adata.uns['category_dict'].keys())
            self.group.value = new_name
            print(self.adata.uns['category_dict'])
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_edit(self))

    # Delete category
    def del_category(self):
        self.button_disabled()
        def next_del(self):
            del self.adata.uns['category_dict'][self.group.value]   
            del self.adata.obs[self.group.value]
            self.group.options = list(self.adata.uns['category_dict'].keys())
            if len(self.group.options) == 0:
                self.group.value = ''
            else:
                self.group.value = self.group.options[0]
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_del(self))

    #### Class Callback Function #####
    # Update the label of class checkbox
    def update_checkbox(self):
        self.button_disabled()
        def updata(self):
            cate = self.group.value
            group_list = self.adata.uns['category_dict'][cate]['class_name']
            #print('=====', group_list[0],group_list[1])
            cls_label = []
            num = 0
            # for i in range(self.adata.uns['category_dict'][cate].shape[0]):
            for i in range(len(group_list)):
                class_name = group_list[i]
                cell_num = len(self.data_df[self.adata.obs[cate]==group_list[i]])       
                s = str(class_name) +  ': cell_nums=' + str(cell_num)
                cls_label = np.append(cls_label,s)
                num = num + cell_num
            cls_label = np.append(cls_label,str('Unassigned: color=grey, cell_nums=' + str(self.data_df.shape[0]-num))) 
            self.class_checkbox.labels = list(cls_label)
            #self.text_color()
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : updata(self))

    def show_checked(self):
        self.button_disabled()
        def next_show(self):
            group = self.group.value
            group_list = self.adata.uns['category_dict'][group]['class_name']
            #source.selected.indices = temp[temp[cat_opt.value]==str(self.class_checkbox.active[0])].index
            self.source.selected.indices = list(self.adata.obs[self.adata.obs[group].isin(list(group_list[i] for i in self.class_checkbox.active))]['ind'])
            self.show_color()
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_show(self))

    # Show color on checkbox
    def text_color(self):
        self.button_disabled()
        def next_text(self):
            color_js = ''
<<<<<<< HEAD
=======
            '''print('\ntext_color: color===')
            print(self.adata.uns['category_dict'][self.group.value]['color'])'''
>>>>>>> extension
            try:
                length = len(self.adata.uns['category_dict'][self.group.value]['color']) 
                for i in range(length):
                    color_js = color_js + self.adata.uns['category_dict'][self.group.value]['color'][i] + ' '
<<<<<<< HEAD
                self.para_color.text = color_js + color_list[18]
            except:
                length = 1
                #color_js = [color_list[18]]
                self.para_color.text = str(color_list[18])
            self.trigger_color.text = self.trigger_color.text + '1'
            #print('CALL',color_js)
=======
                    # print("color_js", color_js)
                self.para_color.text = color_js + color_list[18]
            except:
                print('====text color failed===')
                length = 1
                # color_js = [color_list[18]]
                self.para_color.text = str(color_list[18])
            # trigger js_on_change
            self.trigger_color.text = self.trigger_color.text + '1'
            # print('CALL',color_js)
>>>>>>> extension
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_text(self))

    # Save change of classes
    def save_class(self, cate, class_name, color, n):
        self.button_disabled()
        def save(self, cate):
            if n == 0:
                ind = len(self.class_checkbox.labels)-1
            else:
                ind = self.class_checkbox.active[0]  
            class_label = list(self.adata.obs[cate])
            group_list = self.adata.uns['category_dict'][cate]['class_name']
            print(group_list)
            for i in self.source.selected.indices:
                class_label[i] = group_list[ind]
                #print('i:',i)
            self.adata.obs[cate] = class_label
            #print(class_label)
            cate = self.group.value
            self.update_checkbox()
            self.class_checkbox.active = [ind]
            self.show_color()
            self.correct_func()
            #self.text_color()
            self.button_disabled()
        curdoc().add_next_tick_callback(lambda : save(self, cate))

    # New Class
    def add_entry(self):
        self.button_disabled()
        def next_add_entry(self):
            xaxis = str(self.p.xaxis.axis_label)
            yaxis = str(self.p.yaxis.axis_label)
            #if str(cat_opt.value) != xaxis+'+'+yaxis and str(cat_opt.value) != yaxis+'+'+xaxis:
            if self.group.value == ' ':
                print(str(self.group.value),xaxis+'+'+yaxis)
                #self.class_checkbox.labels = ['no cluster: color=' + color_list[18] + ', cell_nums=' + str(self.data_df.shape[0])]
                def creat_new_group():
                    if self.group_name.value == '':
                        marker = str(self.p.xaxis.axis_label) + '+' + str(self.p.yaxis.axis_label)
                    else:
                        marker = self.group_name.value
                    self.adata.uns['category_dict'][marker] = pandas.DataFrame(columns=['class_name','color','cell_num'])
                    self.adata.obs[marker] = pandas.Series(index=self.data_df.index,dtype=object)
                    self.group.options = list(self.adata.uns['category_dict'].keys())
                    self.group.value = marker
                    print('group:', self.group.value)
                    print('group_name', self.group_name.value)
                    self.group_name.value = '' 
                creat_new_group()
            cell_num = len(self.source.selected.indices)
            print('add cluster: ',self.group.value)
            self.adata.uns['category_dict'][self.group.value].loc[len(self.adata.uns['category_dict'][self.group.value])] = {'class_name':self.class_name.value,'color':self.cur_color,'cell_num':cell_num}
            self.save_class(self.group.value, self.class_name.value, self.cur_color, 0)
            self.class_name.value = ''
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_add_entry(self))

    # Merge checked classes
    def merge(self):
        self.button_disabled()
        def next_merge(self):
            group = self.group.value
            if self.class_name.value == '':
                toclass = self.adata.uns['category_dict'][group]['class_name'][self.class_checkbox.active[0]]
                color = self.adata.uns['category_dict'][group]['color'][self.class_checkbox.active[0]]
            else:
                toclass = self.class_name.value
                color = self.cur_color
            
            cluster_list = self.adata.uns['category_dict'][group]['class_name']
            try:
                for i in self.class_checkbox.active:
                    self.adata.obs[self.group.value] = self.adata.obs[self.group.value].cat.rename_categories({cluster_list[i]: toclass})
            except:
                self.adata.obs.loc[self.adata.obs[group].isin([cluster_list[i] for i in self.class_checkbox.active]), group] = toclass
            count = sum([self.adata.uns['category_dict'][group].loc[i,'cell_num'] for i in self.class_checkbox.active])
            checked_color = [self.adata.uns['category_dict'][group].loc[i,'color'] for i in self.class_checkbox.active]
            self.adata.uns['category_dict'][group].drop(index=self.class_checkbox.active,inplace=True)
            temp = self.adata.uns['category_dict'][group]
            self.adata.uns['category_dict'][group] = pandas.DataFrame(columns=['class_name','color','cell_num'],index=list(range(self.adata.uns['category_dict'][group].shape[0])))
            self.adata.uns['category_dict'][group]['class_name'] = pandas.Series(list(temp['class_name'])) 
            self.adata.uns['category_dict'][group]['color'] = pandas.Series(list(temp['color'])) 
            self.adata.uns['category_dict'][group]['cell_num'] = pandas.Series(list(temp['cell_num'])) 
            self.adata.uns['category_dict'][group].loc[self.adata.uns['category_dict'][group].shape[0]] = {'class_name':toclass,'color':color,'cell_num':count}
            del_list2 = self.class_checkbox.labels
            for i in range(len(self.class_checkbox.active)):
                del del_list2[self.class_checkbox.active[i]-i]
            tt = del_list2[-1]
            del_list2[-1] = str(toclass+ ': cell_nums='+ str(count))
            del_list2 = del_list2 + [tt]
            self.class_checkbox.labels = del_list2
            self.class_checkbox.active = []
            col_list = [color if self.source.data['color'][i] in checked_color else self.source.data['color'][i] for i in range(self.data_df.shape[0])]
            self.source.data['color'] = col_list
            # self.text_color()
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_merge(self))

    # Delete Class
    def del_class(self):
        self.button_disabled()
        def next_del_claass(self):
            group = self.group.value
            cluster_list = self.adata.uns['category_dict'][group]['class_name']
<<<<<<< HEAD
            self.adata.obs.loc[self.adata.obs[group].isin([cluster_list[i] for i in self.class_checkbox.active]),group] = np.nan
            checked_color = [self.adata.uns['category_dict'][group].loc[i,'color'] for i in self.class_checkbox.active]
            self.adata.uns['category_dict'][group].drop(index=self.class_checkbox.active,inplace=True)
            
            del_list2 = self.class_checkbox.labels
            for i in range(len(self.class_checkbox.active)):
                del del_list2[self.class_checkbox.active[i]-i]
            del_list2[-1] = str('unassigned: color=grey, cell_nums=' + str(self.adata.obs.shape[0] - sum(self.adata.uns['category_dict'][group]['cell_num'])))
            self.class_checkbox.labels = del_list2
            self.class_checkbox.active = []
            self.adata.uns['category_dict'][group] = pandas.DataFrame(self.adata.uns['category_dict'][group], index=list(range(self.adata.uns['category_dict'][group].shape[0])))
            col_list = [color_list[18] if self.source.data['color'][i] in checked_color else self.source.data['color'][i] for i in range(self.data_df.shape[0])]
=======
            '''print('\ndel_class: color=0=')
            print(self.adata.uns['category_dict'][group]['color'])'''
            # set obs.group in cluster_list to nan 
            # speed up delete_class 
            # self.adata.obs.loc[self.adata.obs[group].isin([cluster_list[i] for i in self.class_checkbox.active]),group] = np.nan
            self.adata.obs[group][self.adata.obs[group].isin([cluster_list[i] for i in self.class_checkbox.active])] = np.nan
            checked_color = [self.adata.uns['category_dict'][group].loc[i,'color'] for i in self.class_checkbox.active]
            # delete
            self.adata.uns['category_dict'][group].drop(index=self.class_checkbox.active,inplace=True)
            # Reset Index
            self.adata.uns['category_dict'][group].reset_index(drop=True, inplace=True)
            check_box_list = self.class_checkbox.labels
            # special del
            for i in range(len(self.class_checkbox.active)):
                del check_box_list[self.class_checkbox.active[i]-i]
            check_box_list[-1] = str('unassigned: color=grey, cell_nums=' + str(self.adata.obs.shape[0] - sum(self.adata.uns['category_dict'][group]['cell_num'])))
            self.class_checkbox.labels = check_box_list
            self.class_checkbox.active = []
            self.adata.uns['category_dict'][group] = pandas.DataFrame(self.adata.uns['category_dict'][group], index=list(range(self.adata.uns['category_dict'][group].shape[0])))
            col_list = [color_list[18] if self.source.data['color'][i] in checked_color else self.source.data['color'][i] for i in range(self.data_df.shape[0])]
            # print('col_list', col_list)
>>>>>>> extension
            self.source.data['color'] = col_list
            # self.text_color()
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_del_claass(self))

    # Rename class
    def rename(self):
        ind = self.class_checkbox.active[0]
        print('rename ind:',ind)
        cell_num = self.adata.uns['category_dict'][self.group.value]['cell_num'][ind]

        labels = self.class_checkbox.labels
        labels[ind] = str(self.class_name.value) + ': cell_nums=' + str(cell_num)
        old_name = self.adata.uns['category_dict'][self.group.value]['class_name'][ind]
        try:
            self.adata.obs[self.group.value] = self.adata.obs[self.group.value].cat.rename_categories({old_name: self.class_name.value})
        except:
            self.adata.obs.loc[self.adata.obs[self.group.value]==old_name, self.group.value] = self.class_name.value
        self.adata.uns['category_dict'][self.group.value]['class_name'][ind] = self.class_name.value
        self.class_name.value = ''
        print(labels)
        self.class_checkbox.labels = labels

        #self.text_color()

    # Add dots to cluster
    def save_cls_button(self):
        self.button_disabled()
        def next_save(self):
            class_name = self.adata.uns['category_dict'][self.group.value]['class_name'][self.class_checkbox.active[0]]
            color = self.adata.uns['category_dict'][self.group.value]['color'][self.class_checkbox.active[0]]
            cell_num = len(self.source.selected.indices)
            self.save_class(self.group.value, class_name, color, cell_num)
            print(self.adata.uns['category_dict'][self.group.value])
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_save(self))

    # Remove dots from cluster
    def remove_dot(self):
        self.button_disabled()
        def next_remove(self):
            cl_label = self.adata.obs[self.group.value]
            checked_list = list(self.adata.uns['category_dict'][self.group.value].loc[[j for j in self.class_checkbox.active],'class_name'])
            print(checked_list)
            for i in self.source.selected.indices:
                if cl_label[i] in checked_list:
                    cl_label[i] = np.nan
            self.adata.obs[self.group.value] = cl_label
            self.update_checkbox()
            self.show_color()
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_remove(self))

    # Update class
    def update_clus(self):
        self.button_disabled()
        def next_update(self):
            ind = self.class_checkbox.active[0]
            #adata.obs[adata.obs[cat_opt.value]==str(ind)].loc[cat_opt.value] = pandas.Series(index=[0],dtype=object)[0]
            cl_label = self.adata.obs[self.group.value]
            group_list = self.adata.uns['category_dict'][self.group.value]['class_name']
            cl_label[self.adata.obs[self.group.value]==group_list[ind]] = np.NAN
            for i in self.source.selected.indices:
                cl_label[i] = group_list[ind]
            self.adata.obs[self.group.value] = cl_label
            self.update_checkbox()
            self.show_color()
            #self.text_color()
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_update(self))

    # change color of class
    def change_color(self):
        self.button_disabled()
        def next_color(self):
            color_l = self.source.data['color']
            self.show_checked()
            for i in self.source.selected.indices:
                color_l[i] = self.cur_color
            self.source.data['color'] = color_l
            self.adata.uns['category_dict'][self.group.value]['color'][[i for i in self.class_checkbox.active]] = self.cur_color
            self.text_color()
            #print(hide.value,now_color)
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : next_color(self))

    #### Highly variable gene functions #####
    def show_colorbar(self, marker):
        self.button_disabled()
        def show(self, marker):
            if marker:
                updated_color = self.data_df.loc[:,self.ct_marker.value]
            else:
                updated_color = self.data_df.loc[:,self.hl_input.value]
            updated_color = (updated_color-min(updated_color))*(self.hl_bar_map.high - self.hl_bar_map.low)/(max(updated_color)-min(updated_color))
            self.source.data["hl_gene"] = list(updated_color) 
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : show(self, marker))
    
    def hl_filter(self):
        self.button_disabled()
        def h1(self):
            if self.view.filters == []:
                filter_list = list(range(self.data_df.shape[0]))
            else:
                print(self.view.filters)
                filter_list = list(self.view.filters[0].indices)
            if self.hl_filt.value == 'Gene Expression >':
                index_list = list(self.adata.obs[self.data_df[self.hl_input.value] > float(self.hl_filt_num.value)]['ind'])
            elif self.hl_filt.value == 'Gene Expression <':
                index_list = list(self.adata.obs[self.data_df[self.hl_input.value] < float(self.hl_filt_num.value)]['ind'])
            else:
                index_list = list(self.adata.obs[self.data_df[self.hl_input.value] == float(self.hl_filt_num.value)]['ind'])
            index_list = set(index_list)&set(filter_list)
            self.source.selected.indices = list(index_list)
            #new_r = show_colorbar()
            self.r.selection_glyph = Circle(fill_alpha=1,fill_color='Black')
            #print(self.source.selected.indices)
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : h1(self))

    def marker_choice(self):
        self.button_abled()
        def marker(self):
            print('filename change: ',self.marker_file.filename)
            if True:
                marker = pandas.read_csv('data/' + self.marker_file.filename)

                cell_type = list(set(marker['cell_type']))
                print(cell_type)
                self.cell_type.options = ['No cell type'] + cell_type
                self.cell_type.value = cell_type[0]
                #self.change_marker_ct()
            else:
                print('PROBLEM')
                attention = Div(text='No marker gene list found!')
                curdoc().add_root(attention)
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : marker(self))

    def change_marker_ct(self):
        self.button_disabled()
        def ct(self):
            cell_type = self.cell_type.value
            marker = pandas.read_csv('data/' + self.marker_file.filename)
<<<<<<< HEAD
            print('+++++++marker gene')
=======
            # print('+++++++marker gene')
>>>>>>> extension
            marker_list = list(marker[marker['cell_type']==cell_type].loc[:,'marker_gene'])
            self.ct_marker.options = marker_list
            self.ct_marker.value = marker_list[0]
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : ct(self))


    def change_select(self, main_plot):
        main_plot.source.selected.indices = self.source.selected.indices

    def change_view(self,main_plot):
        self.button_disabled()
        def view(self,main_plot):
            self.source.data = dict(main_plot.source.data)
            self.adata = main_plot.adata
            self.data_df = main_plot.data_df
            self.r.glyph.x = main_plot.r.glyph.x
            self.r.glyph.y = main_plot.r.glyph.y
            self.p.xaxis.axis_label = main_plot.p.xaxis.axis_label
            self.p.yaxis.axis_label = main_plot.p.yaxis.axis_label
            self.view.filters = main_plot.view.filters
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : view(self,main_plot))

    #### Other Functions ####
    # Show color of category
    def show_color(self):
        self.button_disabled()
        def color(self):
            col_list = [color_list[18] for i in range(self.data_df.shape[0])]
            #print(col_list)
            for i in range(len(self.adata.uns['category_dict'][self.group.value])):
                #print(self.adata.obs.columns)
                inds = list(self.adata.obs[self.adata.obs[self.group.value]==self.adata.uns['category_dict'][self.group.value]['class_name'][i]]['ind'])
                color = self.adata.uns['category_dict'][self.group.value]['color'][i]
                col_list = [color if j in inds else col_list[j] for j in range(len(col_list))] 
            self.source.data['color'] = col_list
            self.button_abled()
        curdoc().add_next_tick_callback(lambda : color(self))

class data_trans():
    def __init__(self,
                 x_label,
                 data_color,
                 selected_color,
                 checked_class,
                 selected_group,
                 selected_indices,
                 showing_indices
                 ):
        self.data_color = data_color
        self.x_label = x_label
        self.selected_color = selected_color
        self.checked_class = checked_class
        self.selected_group = selected_group
        self.selected_indices = selected_indices
        self.showing_indices = showing_indices




class CreateTool:
    
    def __init__(self,adata):
        self.adata = adata
        self.hl_gene_map = log_cmap('hl_gene', cc.kbc[::-1], low=1, high=20) # color log map

    def set_function(self, effector, attr, value):
        setattr(effector, attr, value)
        
<<<<<<< HEAD
    def base_tool(self):        
        # module_checkbox = CheckboxGroup(labels=load_options(),active=[],name='modules_checkbox') 
        module_select = Select(title='Choose Functions to Add:', options=load_options(), value='', name='modules_select', id='1234') 
        module_select.on_change('value', lambda attr, old, new: load_module(module_select.value))
        Figure = FlowPlot(data=self.adata, color_map='color')

        layout=row(column(Figure.p, Figure.show_gene_list, Figure.show_plot, Figure.para_color, Figure.trigger_color, Figure.extension_url, Figure.import_extension, module_select), # module_checkbox added
=======
    def base_tool(self):       
        global module_select_id 
        # module_checkbox = CheckboxGroup(labels=load_options(),active=[],name='modules_checkbox') 
        module_select = Select(title='Choose Functions to Add:', options=load_options(), value='', name='modules_select', id=str(module_select_id)) 
        module_select.on_change('value', lambda attr, old, new: load_module(module_select.value))
        Figure = FlowPlot(data=self.adata, color_map='color')

        layout=row(column(Figure.p, Figure.show_gene_list, Figure.show_plot, Figure.para_color, Figure.trigger_color, Figure.extension_url, Figure.import_extension, Figure.extension_packages, module_select), # module_checkbox added
>>>>>>> extension
            column(Figure.choose_panel,Figure.s_x, Figure.s_y, Figure.log_axis, Figure.color_selection, Figure.gate_button, Figure.remove_button, Figure.showall_button, Figure.export_button),
            column(Figure.group, Figure.group_name, Figure.create_group, Figure.rename_group, Figure.delete_group,
             Figure.class_name, Figure.new_class, Figure.checkbox_color, Figure.class_checkbox),
            column(Figure.show_selected_class, Figure.add_to, Figure.remove_from, Figure.update_class,
             Figure.rename_class,  Figure.merge_class, Figure.delete_class))

        # attr refers to the changed attribute’s name, and old and new refer to the previous and updated values of the attribute
        # module_checkbox.on_change('active', lambda attr, old, new: load_module(list(module_checkbox.active))) 
        # active: The list of indices of selected check boxes.
        return Figure, layout
    
    def highlight_gene(self, main_plot):
        hl_figure = FlowPlot(data=self.adata, color_map=self.hl_gene_map, main_plot=main_plot,title='Highlight Gene Plot') # input main_plot
        #hl_figure.p.visible = False
        #hl_figure.marker_choice()
        layout = row(hl_figure.p, 
                 column(hl_figure.marker_file, hl_figure.cell_type, hl_figure.ct_marker, hl_figure.show_marker, hl_figure.hl_input, hl_figure.hl_button, 
                 row(hl_figure.hl_filt, hl_figure.hl_filt_num),hl_figure.hl_filt_button,hl_figure.hl_comfirm))

        return hl_figure, layout

    def multi_panel(self, plot_list, panel_list, title_list, update_view=False): # choose two panels
        tab_list = []
        for i in range(len(panel_list)):
            panel = Panel(child=panel_list[i], title=title_list[i])
            tab_list = tab_list + [panel]
        tabs = Tabs(tabs = tab_list)
        if update_view == True:  
           tabs.on_change('active',lambda attr, old, new: plot_list[1].change_view(plot_list[0])) # change view according to the main_plot when get trimmed or gated
        return tabs
    
    def trans_to_json(self, Figure):
        to_json = data_trans(Figure.adata)
        to_json = json.dumps(obj=to_json.__dict__,ensure_ascii=False)
        return to_json

        
color_list = d3['Category20c'][20]
Main_plot = FlowPlot

class connection:
<<<<<<< HEAD
    global extension_path, data_file
=======
    global extensions_path, data_path
>>>>>>> extension
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

    def get_data_df(self):
        return self.Figure.data_df

    def set_anndata(self, adata):
        self.Figure.adata = adata
        data_df = self.Figure.data_df
        data_log = self.Figure.data_log
        if len(data_df.index) != len(self.Figure.adata.obs_names):
            indices = list(set(data_df.index) - set(self.Figure.adata.obs_names))
            data_df.drop(index=indices, axis=0, inplace=True)
            data_log.drop(index=indices, axis=0, inplace=True)
            
        df_column = list(set(data_df.columns) - set(['hl_gene','color']))
        if len(df_column) != len(self.Figure.adata.var_names):
            del_columns = list(set(df_column)-set(self.Figure.adata.var_names))
            data_df.drop(labels=del_columns, axis=1, inplace=True)
            data_log.drop(labels=del_columns, axis=1, inplace=True)
        self.Figure.data_df = data_df
        self.Figure.data_log = data_log
        self.Figure.adata.obs['ind'] = pandas.Series(np.array(range(self.Figure.data_df.shape[0])).astype(int).tolist(), index=self.Figure.data_df.index)
        self.Figure.view.filters = [IndexFilter(list(self.Figure.adata.obs['ind']))]

    def get_group_dict(self):
        return self.Figure.adata.uns['category_dict']
    
    def set_group_dict(self, group_dict):
        self.Figure.adata.uns['category_dict'] = group_dict
    
    def get_obs(self):
        return self.Figure.adata.obs

    def get_obsm(self):
        return self.Figure.adata.obsm
    
    def set_obs(self, group_label, set_group_name=None):
        if not set_group_name:
            self.Figure.adata.obs = group_label
            return 
        try:
            existed_group_list = list(self.Figure.adata.uns['category_dict'].keys()) + ['ind']
        except:
            self.adata.uns['category_dict'] = dict()      
            existed_group_list = ['ind'] 
        group_list = list(group_label.columns)

        for group in set_group_name:
            if True:
                if group in list(self.Figure.adata.uns['category_dict'].keys()):
                    del self.Figure.adata.uns['category_dict'][group]
                    self.Figure.adata.obs.drop(group, axis=1)
                self.Figure.adata.uns['category_dict'][group] = pandas.DataFrame(columns=['class_name','color','cell_num'])
                class_list = group_label[group]
                self.Figure.adata.obs[group] = pandas.Series(group_label[group], dtype=object)
                class_dict = {}
                for value in class_list:
                    class_dict[value] = class_dict.get(value,0) + 1
                ind = 0
                for key in class_dict.keys():
                    self.Figure.adata.uns['category_dict'][group].loc[ind,:] = {'class_name': key, 'cell_num': class_dict[key], 'color':color_list[int(ind*3%20)]}
                    ind = ind + 1
        self.Figure.adata.obs = group_label
        self.Figure.group.options = list(self.Figure.adata.uns['category_dict'].keys())
        self.Figure.group.value = self.Figure.group.options[-1]
        self.Figure.update_checkbox()
        self.Figure.show_color()


    def set_varm(self, varm):
        self.Figure.adata.varm = varm

    def set_uns(self, uns):
        self.Figure.adata.uns = uns
    
    def set_obsm(self, obsm):
        views = list(obsm)
        print('views:', views)
        for view_name in views:
            if view_name not in self.Figure.choose_panel.options:
                for i in range(obsm[view_name].shape[1]):
                    self.Figure.data_df[view_name+str(i)] = pandas.Series(obsm[view_name][:,i],index=self.Figure.data_df.index)
                    self.Figure.data_log[view_name+str(i)] = self.Figure.data_df[view_name+str(i)]
                    #print('data_df===',self.Figure.data_df[view_name+str(i)])
        view_list = list(obsm.keys())+['generic_columns']
        self.Figure.adata.obsm = obsm
        self.Figure.choose_panel.options = view_list
        self.Figure.choose_panel.value = view_list[-2]
        self.Figure.s_x.value = view_list[-2] + str(0)
        self.Figure.s_y.value = view_list[-2] + str(1)
    
<<<<<<< HEAD
    def get_data_file(self):
        return data_file

    def get_extension_file(self):
        return extension_path
=======
    def get_data_path(self):
        return data_path

    def get_extension_file(self):
        return extensions_path
>>>>>>> extension


class plot_function:
    def __init__(self):
        self.Figure = Main_plot
    
    def show_checked(self):
        self.Figure.show_checked()

    def change_checkbox_color(self):
        self.Figure.text_color()

    def get_figure(self):
        return self.Figure.p
    
    def get_x_y(self):
        return self.Figure.s_x.value, self.Figure.s_y.value

    def get_log_axis(self):
        return self.Figure.log_axis
  
    def get_glyph_list(self):
        return self.Figure.glylist
    
    def get_buttons_group(self):
        return self.Figure.buttons_group, self.Figure.buttons_amount
<<<<<<< HEAD
=======

>>>>>>> extension
    def tweak_buttons_group(self, buttons_group):
        self.Figure.buttons_group = buttons_group



# def _load_package(active, layout):    
#     buttons = curdoc().get_model_by_name('module_buttons')
#     try:
#         curdoc().remove_root(buttons)
#     except:
#         print('##### NO MODULE #####')
#     try:
#         options = new_layout().add()
#     except:
#         sys.path = [os.path.dirname(os.path.abspath(__file__))] + sys.path
#         from new_func import new_layout
#         new_class = new_layout()
#         options = new_class.add()

#     #     print(len(options)-i-1)
#     #     curdoc().remove_root(options[len(options)-i-1])
#     # for i in active:
#     #     curdoc().add_root(options[i])
#     layouts = column()
#     for i in range(len(options)):
#         if i in active:
#             layouts = column(layouts, options[i])
#     buttons = layouts
#     buttons.name = 'module_buttons'
#     curdoc().add_root(buttons)

# change path = os.path.dirname(os.path.abspath(__file__)) directly into global variable path_

# get extensions 
def load_options():
<<<<<<< HEAD
    global extension_path
    try:
        name_list = os.listdir(extension_path)
=======
    global extensions_path
    try:
        name_list = os.listdir(extensions_path)
>>>>>>> extension
        # listdir: list of file under the path
    except:
        name_list = []
    return name_list

    
def load_module(active):
<<<<<<< HEAD
    global extension_path
=======
    global extensions_path
>>>>>>> extension
    plot = plot_function()
    buttons_group, buttons_n = plot.get_buttons_group() # buttons group, buttons number
    # delete last extended buttons
    for i in range(buttons_n, len(buttons_group)):
        buttons_group.pop()
    # buttons = curdoc().get_model_by_name('module_buttons')
    try:
<<<<<<< HEAD
        name_list = os.listdir(extension_path)
=======
        name_list = os.listdir(extensions_path)
>>>>>>> extension
    except:
        return     
    layouts = column()
    print('active:',active) # ex => active: Clustering_with_Scanpy
    ind = 0 
    for name in name_list:
        but = curdoc().get_model_by_name(name)
        div = Div(text='')
        if name == active:
<<<<<<< HEAD
            sys.path.append(extension_path)
=======
            sys.path.append(extensions_path)
>>>>>>> extension
            module_name = name + '.module'
            try:
                new_class = module_name.new_layout()
            except:            
                mod = importlib.import_module(module_name) # usual way
                new_class = mod.new_layout()
            # clear = Button(label='Clear the figures!', button_type='warning', name=str(ind))
            # clear.on_click(lambda: clear_cb(clear.name))
            # new_buttons = column(new_class.add(), clear)
            new_buttons = column(new_class.add()) 
            # append extended buttons
<<<<<<< HEAD
            buttons_group = find_buttons(new_buttons, buttons_group)
=======
            buttons_group = add_to_buttons_group(new_buttons, buttons_group)
>>>>>>> extension
            plot.tweak_buttons_group(buttons_group)
            if but != None and but.visible == False:
                but.visible = True # already created model
                
                but.children.append(div)
                continue
            if but != None and but.visible == True:
                continue
            print('new_buttons:', new_buttons)
            new_buttons.sizing_mode = 'scale_height'
            new_buttons.name = name
            new_buttons.children.append(div)
            curdoc().add_root(new_buttons)
            layouts = column(layouts, new_buttons)
        else:
<<<<<<< HEAD
            if but != None:
                but.visible = False
=======
            if but is not None:
                curdoc().remove_root(but)
            '''if but != None:
                but.visible = False'''
>>>>>>> extension
        ind = ind + 1
    buttons = layouts
    if curdoc().get_model_by_name('module_buttons') == None:
        buttons.name = 'module_buttons'
    # curdoc().add_root(buttons)

<<<<<<< HEAD
def find_buttons(buttons, buttons_group):
    for child in buttons.children:
        try:
            find_buttons(child, buttons_group)
=======
def add_to_buttons_group(buttons, buttons_group):
    for child in buttons.children:
        try:
            add_to_buttons_group(child, buttons_group)
>>>>>>> extension
        except:
            buttons_group.append(child)

    return buttons_group

<<<<<<< HEAD
=======
def load_extension_select():
    global module_select_id
    # Remove Extensions Visible Buttons
    name_list = os.listdir(extensions_path)  
    for name in name_list:
        but = curdoc().get_model_by_name(name)
        # print("but", but)
        if but is not None:
            curdoc().remove_root(but)
    # Add New Extension Select To Curdoc
    models = curdoc().get_model_by_id(str(module_select_id))
    module_select_id += 1 
    models.visible = False
    curdoc().remove_root(models)
    module_select = Select(title='Choose Functions to Add:', options=load_options(), value='', id=str(module_select_id), name='modules_select')

    module_select.on_change('value', lambda attr, old, new: load_module(module_select.value))
    curdoc().add_root(module_select)

>>>>>>> extension
def clear_cb(ind):
    module_checkbox = curdoc().get_model_by_name('modules_checkbox') 
    # options = module_checkbox.labels
    # for i in range(len(options)):
    #     if options[i] == 'Find_Marker_Gene':
    #         ind = i
    option = module_checkbox.value
    models = curdoc().get_model_by_name(option)
    curdoc().remove_root(models)
    print(curdoc().get_model_by_name(option))
    load_module(module_checkbox.value)
    # models.visible = False
    # module_checkbox.active.remove(int(ind))

def upload_callback(): 

<<<<<<< HEAD
    global extension_path
    global data_file
=======
    global data_path
>>>>>>> extension
    global Main_plot

    # path_, file_name = fetch()
    loading_remind = Div(text='Loading data……')
    curdoc().add_root(loading_remind) 
    print('===loading finished=====')
<<<<<<< HEAD
    filename = os.path.split(data_file)[1]   

    def load():
        global Main_plot
        filetype = os.path.splitext(filename)[-1][1:] # split the filename and the type
                                                      # [-1] means the last tuple: the type 
        if filetype == 'csv':
            adata = sc.read_csv(data_file) 
            print('csv')
        elif filetype == 'h5ad':
            # adata = sc.read_h5ad(data_file)
            adata = anndata.read(data_file, backed='r')
            print('h5ad')
        elif filetype == 'mtx':
            adata = sc.read_10x_mtx(
                'data/hg19/',  # the directory with the `.mtx` file
                var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
                cache=True)                              # write a cache file for faster subsequent reading
        print(data_file)
=======
    filename = os.path.split(data_path)[1]   

    def load():
        global Main_plot
        filetype = os.path.splitext(filename)[-1][1:] # split the filename and the type, [-1] means the last tuple: the type 
        print('filetype:', filetype)
        if filetype == 'csv':
            adata = sc.read_csv(data_path) 
            print('csv data')
        elif filetype == 'h5ad':
            adata = sc.read_h5ad(data_path)
            # adata = anndata.read(data_path, backed='r')  
            print('h5ad data')
        elif filetype == '':
            print("read_10x")
            adata = sc.read_10x_mtx(
                data_path,# the directory with the `.mtx` file
                var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
                cache=True)                              # write a cache file for faster subsequent reading

>>>>>>> extension
        # Figure, layout
        mainplot, panel1 = CreateTool(adata=adata).base_tool() # Mainplot: figure, layout
        print('===mainplot finished=====')
        Main_plot = mainplot
        # Highlight Gene Figure
        hl_figure, panel2 = CreateTool(adata=adata).highlight_gene(mainplot)
        print('====highlight finished=====')
        tab = CreateTool(adata).multi_panel([mainplot,hl_figure], [panel1,panel2], ['Main View', 'Highlight Gene'], update_view=True)
        print('====tab====')
<<<<<<< HEAD
=======

>>>>>>> extension
        curdoc().remove_root(loading_remind)
        curdoc().add_root(tab)
        print('===finish===')

    curdoc().add_next_tick_callback(load)

<<<<<<< HEAD

def text_cover(dir, msg):
    path = dir + '/data_file.txt'
    print("-========- path:", path)
=======
def text_cover(dir, msg):
    path = dir + '/data_file.txt'
    # print("-========- path:", path)
>>>>>>> extension
    with open(path, "w") as f:
        f.truncate(0)
        f.close()
    file = open(path, 'w')
    file.write(msg)
    file.close()

<<<<<<< HEAD

def openreadtxt(dir):
    e_file = open(dir + '/' + 'extension_path.txt', 'r')
    e_path = e_file.readline()
    e_file.close()
    print('-======- e_path:', e_path)
    d_file = open(dir + '/' + 'data_file.txt', 'r')
    data = d_file.readline()
    print('-======- data:', data)
    d_file.close()
    return e_path, data


def get_save_path(dir):
    s_file = open(dir + '/' + 'save_path.txt', 'r')
    s_path = s_file.readline()
    s_file.close()
    print('-======- s_path', s_path)
    return s_path


def main(doc):
    global Main_plot, extension_path, data_file, dir
    appname = "scpantheon"
    appauthor = "xinzhu"
    version = "0.2.1"
    dirs = AppDirs(appname, appauthor, version)
    dir = dirs.user_data_dir
    # read path_ and file from user_data_dir
    extension_path, data_file = openreadtxt(dir)                                                                                              
=======
def main(doc):
    global Main_plot, extensions_path, data_path, module_select_id
    module_select_id = 1999
    # read path_ and file from user_data_dir
    extensions_path, data_path = read_path(dir)
    # auto_pip_install(extensions_path)    
    doc.add_next_tick_callback(upload_callback)                                                     
>>>>>>> extension
    
    '''
    global mycursor
    try: myconnect()
    except:
        try: creatbase() 
        except: ()
    try: creatable()
    except: ()
    try:
        path_, file_name = fetch()
    except:
        print('Please Choose your Extensions and Data paths\n')
        Error_remind = Div(text='Please Choose your Extensions and Data path...')
        doc.add_root(Error_remind)
    '''
    '''print('curdoc:',curdoc(),'\ndoc:', doc)
    upload_button = Button(label="Show")
    upload_button.on_event(ButtonClick, upload_callback)
    curdoc().add_root(upload_button) # 这就是那个按钮'''

<<<<<<< HEAD
    doc.add_next_tick_callback(upload_callback)

    
=======
>>>>>>> extension
if __name__ == "main":
    main(curdoc())

'''
def myconnect():
    global mydb,mycursor
    mydb = mysql.connector.connect(
        host="localhost",
        #  port=3360,
        user="root",
        password="1122cccc",
        database = "mybase"
    )
    mycursor = mydb.cursor()

def creatbase():
    global mycursor, mydb
    mycursor.execute("CREATE DATABASE mybase")
    mydb.database = "mybase"

def creatable():
    global mycursor,mydb
    mycursor.execute("CREATE TABLE vlist (value VARCHAR(255))")
    mydb.commit()

def fetch():
    mycursor.execute("SELECT value FROM vlist")
    result = mycursor.fetchall()
    print("=== mysql test ===")
    print('extension path:(',result[-2][0],')')
    print('Data path:(',result[-1][0],')')
    print("=== test finished ===")
    return result[-2][0], result[-1][0]
<<<<<<< HEAD
'''
=======
'''
 
'''def read_path(dir):
    e_file = open(dir + '/' + 'extensions_path.txt', 'r')
    e_path = e_file.readline()
    e_file.close()
    # print('-======- e_path:', e_path)
    d_file = open(dir + '/' + 'data_file.txt', 'r')
    data = d_file.readline()
    # print('-======- data:', data)
    d_file.close()
    return e_path, data'''
 
'''def get_save_path(dir):
    s_file = open(dir + '/' + 'save_path.txt', 'r')
    s_path = s_file.readline()
    s_file.close()
    # print('-======- s_path', s_path)
    return s_path'''
>>>>>>> extension
