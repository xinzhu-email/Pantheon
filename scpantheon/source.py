from bokeh.io import curdoc
from bokeh.models import Div, Select, Button, TextInput
from bokeh.layouts import column
from basicwidgits import Widgets
import os
from subprocess import check_call
import importlib
import sys
import tabs as tb
import data as dt
try:
    from scpantheon.front_end import extensions_qt 
    from scpantheon.front_end.extensions_qt import get_extensions_path
    from scpantheon.front_end import save_qt, load_qt
    from scpantheon.front_end.data_qt import dir, extract_online_packages, auto_pip_install, read_path
    from scpantheon.front_end.save_qt import get_save_path
except:
    check_call(['pip3', 'install', "scpantheon"])
    from scpantheon.front_end import extensions_qt 
    from scpantheon.front_end.extensions_qt import get_extensions_path
    from scpantheon.front_end import save_qt, load_qt
    from scpantheon.front_end.data_qt import dir, extract_online_packages, auto_pip_install, read_path
    from scpantheon.front_end.save_qt import get_save_path


class Extension:
    
    def __init__(self):
        """
        self.extensions_path: str, a variable to record path of extensions
        self.extensions_list: list(str), a variable to record for module selection
        self.widget_ext_dict: dict("Button_names" : Buttons), record whole info of 4 buttons
        self.layout: Layout, organize 4 buttons for visualization
        """
        self.extensions_path = None
        self.extensions_list = ['Please load an extension']
        self.widget_ext_dict = dict()
        self.init_widget_ext()
        self.init_modules()
        self.load_module()
        self.update_layout()

    def init_widget_ext(self):
        """
        init 3 widgets for extensions
        """
        extension_url = TextInput(title='Extension url: ', value='')
        # self.extension_url.js_on_change("value", CustomJS(code="""
        #     console.log('text_input: value=' + this.value, this.toString())
        # """))
        online_extension = Button (label = "online extension zip")
        # import_extension.on_click(load_online_extensions)
        local_extension = Button(label="local extension packages")
        local_extension.on_click(lambda : self.load_local_extensions())
        self.widget_ext_dict = {
            'extension_url': extension_url,
            'online_extension': online_extension,
            'local_extension': local_extension
            }

    def load_local_extensions(self):
        check_code = extensions_qt.main()
        if check_code == 'app closed':
            self.extensions_path = get_extensions_path(dir) + '/'
        try:
            self.extensions_list = ['Please select a function'] + os.listdir(self.extensions_path)
        except:
            self.extensions_list = ['Please load an extension']
        self.init_modules()
        self.update_layout()
    
    def init_modules(self):
        modules_select = Select(
            title = 'Choose Functions to Add:', 
            options = self.extensions_list,
            value = self.extensions_list[0] if self.extensions_list else '',
            name = 'modules_select',
        )
        modules_select.on_change('value', lambda attr, old, new: self.load_module())
        self.widget_ext_dict['modules_select'] = modules_select
    
    def update_layout(self):
        tb.ext_layout = column(list(self.widget_ext_dict.values()))
        tb.view_panel(tb.panel_dict, tb.ext_layout, tb.curpanel)
    
    def load_module(self):
        """
        create a Widget if not in cls.panel_dict
        """
        module_name = self.widget_ext_dict['modules_select'].value
        if module_name == 'Please select a function' or module_name == 'Please load an extension':
            module_name = 'gene relations'
        tb.curpanel = module_name
        if tb.curpanel in tb.panel_dict:
            curmap = tb.panel_dict[tb.curpanel].widgets_dict['choose_map'].value
            print(dt.adata.uns.keys())
            maplist = list(dt.adata.uns.keys())
            if curmap in maplist:
                new_map = Select(
                    title = 'Choose map:',
                    value = curmap,
                    options = maplist
                )
                tb.panel_dict[tb.curpanel].widgets_dict['choose_map'] = new_map
                new_map.on_change('value',lambda attr, old, new :tb.panel_dict[tb.curpanel].update_var())
                tb.panel_dict[tb.curpanel].update_layout()
            else:
                print("Error: original map is no longer in the new maplist")
        elif module_name == 'gene relations':
            print("init")
            cur_panel = Widgets()
            tb.panel_dict['gene relations'] = cur_panel
            tb.curpanel = 'gene relations'
        else:
            sys.path.append(self.extensions_path)
            name = module_name
            module_name = name + '.module'           
            mod = importlib.import_module(module_name)
            cur_panel = mod.Widgets_Color()
            if cur_panel.new_panel: 
                tb.panel_dict[name] = cur_panel
                tb.curpanel = name
            else: 
                tb.panel_dict['gene relations'] = cur_panel
                tb.curpanel = 'gene relations'
        tb.view_panel(tb.panel_dict, tb.ext_layout, tb.curpanel)


def upload_callback():
    Extension()


def main(doc): 
    """store all data and widgets to show in the doc"""
    
    """starting page with loading remind"""
    loading_remind = Div(text='Loading data……')
    doc.add_root(loading_remind) 
    print('===loading finished=====')

    """init page"""
    # init data
    # Panel_Handler.get_extension()
    # Panel_Handler.init_modules()
    
    """update main page"""
    doc.add_next_tick_callback(upload_callback)                                                     

if __name__ == "main":
    main(curdoc())

 