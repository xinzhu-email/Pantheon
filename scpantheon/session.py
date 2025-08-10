import os
from bokeh.models import Tabs, TabPanel
from scpantheon.globals import dir
from scpantheon.widgets.extPicker import ExtensionPicker
from scpantheon.buttons import make_layout, make_widget, Widget_type
from scpantheon.streamline import Homepage
from scpantheon.tabs import refresh
from bokeh.io import curdoc
import stdata as dt

class Session:
    def __init__(self):
        dt.session_dict = dict()
        dt.session_dict = dt.extract_streamline()
        self.streamline_panel = ExtensionPicker("Quality Control")
        self.synchronize = make_widget(
            Widget_type.button, 
            lambda: self.synchronize_callback(),
            label = "Synchronize Visualization"
            )
        self.visualization = Homepage()
        streamline_tablist = list()
        streamline_list = dt.sort_streamline_list()
        for key in streamline_list:
            tab_layout = make_layout([self.streamline_panel.layout, self.synchronize])
            streamline_tablist.append(TabPanel(child = tab_layout, title = key))
        self.streamline_tab = Tabs(tabs = streamline_tablist)
        self.streamline_tab.tabs_location = "left"
        self.streamline_tab.on_change('active',lambda attr, old, new : self.streamline_tab_callback(attr, old, new))

    
    
    """callbacks"""
    def synchronize_callback(self):
        pass
    
    def streamline_tab_callback(self, attr, old, new):
        refresh_id_panel = self.streamline_panel.layout.id
        refresh_id_prereq = self.streamline_panel.navigation.prereq_plot.p.id
        refresh_id_res = self.streamline_panel.navigation.res_plot.p.id
        new_streamline = dt.sort_streamline_list()[new]
        self.streamline_panel.switch_streamline_callback(new_streamline)
        refresh(refresh_id_panel, self.streamline_panel.layout)
        refresh(refresh_id_prereq, self.streamline_panel.navigation.prereq_plot.p)
        refresh(refresh_id_res, self.streamline_panel.navigation.res_plot.p)

        
    
    