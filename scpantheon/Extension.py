from bokeh.models import Select, Button, TextInput
from bokeh.layouts import column
from bokeh.io import curdoc
from widgets import Widgets
from hlwidgets import Hlwidgets
import os
from subprocess import check_call
import importlib
import sys
import tabs as tb
import data as dt
try:
    from scpantheon.front_end import extensions_qt 
    from scpantheon.front_end.extensions_qt import get_extensions_path
    from scpantheon.front_end import load_qt, save_qt
    from scpantheon.front_end.data_qt import dir, extract_online_packages, read_path

except:
    check_call(['pip3', 'install', "scpantheon"])
    from scpantheon.front_end import extensions_qt 
    from scpantheon.front_end.extensions_qt import get_extensions_path
    from scpantheon.front_end import  load_qt, save_qt
    from scpantheon.front_end.data_qt import dir, extract_online_packages, read_path


class Extension:
    widget_ext_dict = dict()
    print("ext")
    def __init__(self):
        """
        self.extensions_path: str, a variable to record path of extensions
        self.extensions_list: list(str), a variable to record for module selection
        cls.widget_ext_dict: dict("Button_names" : Buttons), record whole info of 4 buttons
        """
        print("source")
        self.extensions_path = None
        self.extensions_list = ['Please load an extension']
        self.init_widget_ext()
        self.init_modules()
        self.init_save()
        self.load_module()
        self.update_layout()

    def init_widget_ext(self):
        """
        init 3 widgets for extensions
        """
        extension_url = TextInput(title='Extension url: ', value='')
        online_extension = Button (label = "online extension zip")
        online_extension.on_click(lambda : self.load_online_extensions())
        local_extension = Button(label="local extension packages")
        local_extension.on_click(lambda : self.load_local_extensions())
        Extension.widget_ext_dict = {
            'extension_url': extension_url,
            'online_extension': online_extension,
            'local_extension': local_extension
            }
        tb.ext_widgets = Extension.widget_ext_dict

    def load_online_extensions(self):
        # Test failed (connection)
        tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        def load_online_extensions_callback(self):
            if Extension.widget_ext_dict['extension_url'].value == '':
                print("Warning: default url as 'https://github.com/xinzhu-email/Pantheon/archive/refs/heads/main.zip'")
                zip_file_url = None
            else:
                zip_file_url = Extension.widget_ext_dict['extension_url'].value
            Extension.widget_ext_dict['extension_url'].value = ''
            check_code = load_qt.main()
            if check_code == 'app closed':
                extract_path = load_qt.get_load_path() + '/online_extension/'
                self.extensions_path, _ = read_path(dir)
                if zip_file_url:
                    extract_online_packages(self.extensions_path, extract_path, zip_file_url)
                else:
                    extract_online_packages(self.extensions_path, extract_path)
            try:
                self.extensions_list = ['Please select a function'] + os.listdir(self.extensions_path)
            except:
                self.extensions_list = ['Please load an extension']
            self.init_modules()
            self.update_layout()
            tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        curdoc().add_next_tick_callback(lambda: load_online_extensions_callback(self))
    
    def load_local_extensions(self):
        tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        def load_local_extensions_callback(self):    
            check_code = extensions_qt.main()
            if check_code == 'app closed':
                self.extensions_path = get_extensions_path(dir) + '/'
            try:
                self.extensions_list = ['Please select a function'] + os.listdir(self.extensions_path)
            except:
                self.extensions_list = ['Please load an extension']
            self.init_modules()
            self.update_layout()
            tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        curdoc().add_next_tick_callback(lambda: load_local_extensions_callback(self))
    
    def init_modules(self):
        modules_select = Select(
            title = 'Choose Functions to Add:', 
            options = self.extensions_list,
            value = self.extensions_list[0] if self.extensions_list else '',
            name = 'modules_select',
        )
        modules_select.on_change('value', lambda attr, old, new: self.load_module())
        Extension.widget_ext_dict['modules_select'] = modules_select
        tb.ext_widgets = Extension.widget_ext_dict
    
    def init_save(self):
        save_data = Button(label='Export Results')
        save_data.on_click(lambda : self.save_data())
        Extension.widget_ext_dict['save_data'] = save_data
        tb.ext_widgets = Extension.widget_ext_dict

    def save_data(self):
        tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        def save_data_callback():
            check_code = save_qt.main()
            if check_code == 'app closed':
                # print('choosing finished')
                path = save_qt.get_save_path(dir) + '/'
                save_qt.text_cover(dir, path + 'result.h5ad') # write the output anndata to cover the data
                print("path covered to " + path + "result.h5ad")
                if not os.path.exists(path):
                    os.makedirs(path)
                for col in dt.adata.obs.columns:
                    if dt.adata.obs[col].dtype != 'category':
                        dt.adata.obs[col] = dt.adata.obs[col].astype('category')
                store_data = dt.adata
                del store_data.uns['group_dict']
                store_data.write_h5ad(path + "result.h5ad")
            tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        curdoc().add_next_tick_callback(lambda: save_data_callback())

    def update_layout(self):
        tb.ext_layout = column(list(Extension.widget_ext_dict.values()))
        tb.view_panel(tb.panel_dict, tb.ext_layout, tb.ext_widgets, tb.curpanel)
    
    def load_module(self):
        """
        create a Widget if not in cls.panel_dict
        """
        tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        def load_module_next(self):
            module_name = Extension.widget_ext_dict['modules_select'].value
            if module_name == 'Please select a function' or module_name == 'Please load an extension':
                module_name = 'gene relations'
            if module_name == tb.curpanel:
                return
            tb.curpanel = module_name
            if tb.curpanel in tb.panel_dict:
                tb.panel_dict[tb.curpanel].switch_tab()
            elif module_name == 'gene relations':
                cur_panel = Widgets(module_name)
                tb.panel_dict['gene relations'] = cur_panel
                tb.curpanel = 'gene relations'
            else:
                sys.path.append(self.extensions_path)
                name = module_name
                module_name = name + '.module'           
                mod = importlib.import_module(module_name)
                cur_panel = mod.Widgets_Color(name)
                if cur_panel.new_panel: 
                    tb.panel_dict[name] = cur_panel
                    tb.curpanel = name
                else: 
                    tb.panel_dict['gene relations'] = cur_panel
                    tb.curpanel = 'gene relations'
            if 'spatial' in dt.adata.obsm_keys() and 'spatial' not in tb.panel_dict:
                hlpanel = Hlwidgets('highlight spatial')
                tb.panel_dict['highlight spatial'] = hlpanel
            tb.view_panel(tb.panel_dict, tb.ext_layout, tb.ext_widgets, tb.curpanel)
            tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        curdoc().add_next_tick_callback(lambda : load_module_next(self))
    
