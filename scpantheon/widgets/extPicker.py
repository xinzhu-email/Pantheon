from scpantheon.buttons import Widget_type, LayoutOrientation, make_widget, make_layout
from scpantheon.globals import dir
from scpantheon.widgets.navigation import Tracker, AdataVis, Stage
from scpantheon.stdata import ExtInfo
from scpantheon.tabs import refresh, refresh_layout
from bokeh.io import curdoc
import stdata as dt
import os
import importlib

def load_module_and_create_instance(module_path, class_name, func_name, ext_name):
    try:
        spec = importlib.util.spec_from_file_location(class_name, module_path)
        if spec is None:
            raise ImportError(f"Could not load spec from {module_path}")
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        if hasattr(mod, class_name):
            cls = getattr(mod, class_name)
            return cls(func_name, ext_name)
        else:
            raise AttributeError(f"Module does not contain class: {class_name}")
    except Exception as e:
        print(f"Error loading module: {e}")
        return None

class Navigation:
    def __init__(self):
        self.prereq_plot = AdataVis(Stage.PREREQUISITE, active=[])
        self.res_plot = AdataVis(Stage.PREREQUISITE, active=[])
        self.tracker = Tracker()
        self.layout = make_layout([
            self.prereq_plot.layout, self.res_plot.layout, 
            self.tracker.layout])

class ExtensionPicker:
    def __init__(self, streamline: str):
        self.streamline = streamline
        self.switch_streamline(self.streamline)
        self.navigation = Navigation()
        self.init_widget_dict()
        self.load_module()
        self.layout = self.init_layout()
    
    def init_widget_dict(self):
        self.ext_title = make_widget(
            Widget_type.div,
            text = "<div style='font-size: 40px;'>" + self.streamline + " Extensions"
        )
        self.method_download = make_widget(
            Widget_type.button,
            lambda: self.ext_download_callback(),
            label = 'Download Online Extensions for ' + self.streamline
        )
        self.method_update = make_widget(
            Widget_type.button,
            lambda: self.ext_update_callback(),
            label = 'Load/Reload Extensions for ' + self.streamline
        )
        self.method_select = make_widget(
            Widget_type.select, 
            lambda: self.ext_select_callback(), 
            title = 'Choose ' + self.streamline + ' Method', 
            options = self.methodlist, 
            value = self.curmethod
            )
        self.session_name = make_widget(
            Widget_type.text,
            lambda: None,
            title = "Name/Rename Session"
        )
        self.session_create = make_widget(
            Widget_type.button,
            lambda: self.session_create_callback(),
            label = "Create Session"
        )
        self.session_rename = make_widget(
            Widget_type.button,
            lambda: self.ext_rename_callback(),
            label = "Rename Session"
        )
        self.session_title = make_widget(Widget_type.div, None, text = f"Sessions for {self.streamline}")
        self.session_select = make_widget(
            Widget_type.select,
            lambda: self.session_select_callback(),
            options = self.sessionlist,
            value = self.cursession
        )
        self.prereq_confirm = make_widget(
            Widget_type.button, 
            lambda: self.prereq_confirm_callback(),
            label = "Confirm Prerequisite Selection"
        )
        

    def init_layout(self):
        return make_layout([self.ext_title, self.method_download, self.method_update, self.method_select,
                            self.session_name, self.session_create, self.session_rename, self.session_select, self.session_title,
                            dt.session_dict[self.streamline][self.curmethod][self.cursession].ext_title,
                            dt.session_dict[self.streamline][self.curmethod][self.cursession].prereq.layout,
                            self.prereq_confirm,
                            dt.session_dict[self.streamline][self.curmethod][self.cursession].layout,
                            dt.session_dict[self.streamline][self.curmethod][self.cursession].res.layout
                            ])
            
    

    """callback"""
    def ext_select_callback(self):
        pass

    def ext_update(self): 
        extensions_path = os.path.join(dir, 'extensions', self.streamline)
        if not os.path.exists(extensions_path):
            os.mkdir(extensions_path)
        if os.listdir(extensions_path) == []:
            extensions_list = ['No local extensions']
        else:
            extensions_list = os.listdir(extensions_path)
        print("extension updated")
        return extensions_list
    
    def ext_update_callback(self):
        self.ext_update()
        # tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        # def ext_update_next():
        #     self.ext_update()
        #     tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)       
        # curdoc().add_next_tick_callback(lambda: ext_update_next())

    def ext_download_callback(self):
        pass

    def session_create_callback(self):
        if self.session_name.value in self.sessionlist:
            print(f"Rejected: session {self.session_name.value} already exists, change another name")
            self.session_name.value = ""
            refresh_id = self.session_name.id
            refresh(refresh_id, self.session_name)
            return
        last_session = self.cursession
        self.cursession = self.session_name.value
        self.sessionlist.append(self.cursession)
        self.session_select.options = self.sessionlist 
        refresh_id = dt.session_dict[self.streamline][self.curmethod][last_session].layout.id
        refresh_id_title = dt.session_dict[self.streamline][self.curmethod][last_session].ext_title.id
        self.load_module(self.cursession)
        self.session_name.value = ""
        self.session_select.value = self.cursession
        refresh(refresh_id, dt.session_dict[self.streamline][self.curmethod][self.cursession].layout)
        refresh(refresh_id_title, dt.session_dict[self.streamline][self.curmethod][self.cursession].ext_title)
    
    def ext_rename_callback(self):
        pass

    def session_select_callback(self):
        refresh_id = dt.session_dict[self.streamline][self.curmethod][self.cursession].layout.id
        refresh_id_title = dt.session_dict[self.streamline][self.curmethod][self.cursession].ext_title.id
        self.cursession = self.session_select.value
        refresh(refresh_id_title, dt.session_dict[self.streamline][self.curmethod][self.cursession].ext_title)
        refresh(refresh_id, dt.session_dict[self.streamline][self.curmethod][self.cursession].layout)
    
    def switch_streamline_callback(self, streamline: str):
        self.streamline = streamline
        self.switch_streamline(self.streamline)
        self.init_widget_dict()
        self.load_module()
        self.layout = self.init_layout()
    
    def prereq_confirm_callback(self):
        # TODO: build an Anndata
            # a) get .obs_names, .var_names from selection
        data_kwarg = dict()
        data_kwarg['var_valid'] = dt.validcache.valid_var
        data_kwarg['obs_valid'] = dt.validcache.valid_obs
        total_key = []
        for i in range(dt.session_dict[self.streamline][self.curmethod][self.cursession].prereq.n_req):
            res_key = dt.session_dict[self.streamline][self.curmethod][self.cursession].prereq.widgets_dict[f"select_result_{i}"].value
            total_key.append(res_key)
            if dt.session_dict[self.streamline][self.curmethod][self.cursession].prereq.data_type[i][0].value not in list(data_kwarg.keys()):
                data_kwarg[dt.session_dict[self.streamline][self.curmethod][self.cursession].prereq.data_type[i][0].value] = [res_key]
            else:
                data_kwarg[dt.session_dict[self.streamline][self.curmethod][self.cursession].prereq.data_type[i][0].value].append(res_key)
            # c) copy & filter selected results to new adata
        new_data = dt.ExtAdataManager(dt.adata, **data_kwarg)
        dt.session_dict[self.streamline][self.curmethod][self.cursession].data = new_data.make_ext_data(dt.adata).copy()
        print(dt.session_dict[self.streamline][self.curmethod][self.cursession].data)
        refresh_id_tracker = dt.digplot.plot.id
        dt.digplot.update_node_valid(
            self.cursession, 
            dt.validcache.valid_var, 
            dt.validcache.valid_obs
        )
        dt.digplot.update_node_by_dataframe(
            self.cursession, 
            dt.session_info, 
            parents = True, 
            parentlist = total_key
        )
        dt.digplot.make_plot()
        refresh(refresh_id_tracker, dt.digplot.plot)

    
    """functional"""
    def load_module(self, module_name: str | None = None, in_curdoc: bool = False):
        method = self.method_select.value
        if module_name:
            session = module_name
        else:
            session = self.session_select.value
        if method == 'No local extensions':
            return
        module_path = os.path.join(dir, 'extensions', self.streamline, method, 'module.py')       
        class_name = "PanelExt"
        refresh_id_pre = self.navigation.prereq_plot.p.id
        refresh_id_res = self.navigation.res_plot.p.id
        refresh_id_tracker = dt.digplot.plot.id
        if (self.cursession not in dt.session_dict[self.streamline][self.curmethod]) or (dt.session_dict[self.streamline][self.curmethod][self.cursession] is None):
            dt.digplot.add_node(ExtInfo(self.cursession, self.streamline))
            dt.digplot.update_node_valid(self.cursession, dt.adata.var_names, dt.adata.obs_names)
            dt.digplot.make_plot()
        dt.session_dict[self.streamline][self.curmethod][self.cursession] = load_module_and_create_instance(module_path, class_name, self.streamline, session)
        self.update_navigation()
        if in_curdoc is False:
            refresh_layout(refresh_id_pre, self.navigation.prereq_plot.p, self.navigation.layout)
            refresh_layout(refresh_id_res, self.navigation.res_plot.p, self.navigation.layout)
            refresh_layout(refresh_id_tracker, dt.digplot.plot, self.navigation.layout)
        else:
            refresh(refresh_id_pre, self.navigation.prereq_plot.p)
            refresh(refresh_id_res, self.navigation.res_plot.p)
            refresh(refresh_id_tracker, dt.digplot.plot)
        self.curmethod = method # just in case
        self.cursession = session # just in case
    
    def switch_streamline(self, streamline):
        self.methodlist = list(dt.session_dict[streamline].keys())
        if self.methodlist == []: # theoratically impossible
            print(f"{streamline} Has No Extension Loaded")
            return
        self.curmethod = self.methodlist[0]
        if len(dt.session_dict[streamline][self.curmethod]) == 0:
            dt.session_dict[streamline][self.curmethod][f"{self.curmethod} Session 0"] = None
        self.sessionlist = list(dt.session_dict[streamline][self.curmethod].keys())
        self.cursession = self.sessionlist[0]
        
    def update_navigation(self):
        print(247, self.cursession)
        input_type = [prompt_tuple[0] for prompt_tuple in dt.session_dict[self.streamline][self.curmethod][self.cursession].prereq.data_type]
        input_type_unique = list(set(input_type))
        result_type = [prompt_tuple[0] for prompt_tuple in dt.session_dict[self.streamline][self.curmethod][self.cursession].res.data_type]
        result_type_unique = list(set(result_type))
        self.navigation.prereq_plot.update_active(input_type_unique)
        self.navigation.res_plot.update_active(result_type_unique)

