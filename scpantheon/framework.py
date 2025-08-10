from bokeh.models import Tabs, TabPanel
from bokeh.plotting import curdoc
from scpantheon.buttons import make_layout, LayoutOrientation
from scpantheon.widgets.console import Console
from scpantheon.widgets.export import Export
from scpantheon.session import Session


class Framework:
    def __init__(self):
        self.console = Console()
        self.export = Export()
        self.session = Session()
        self.layout = self.init_layout()
        self.view_panel()
    
    def init_layout(self):
        navigation_panel = TabPanel(child = self.session.streamline_panel.navigation.layout, title = "navigation")    
        console_panel = TabPanel(child = self.console.layout, title = "console")
        export_panel = TabPanel(child = self.export.layout, title = "export")
        homepage_tabs = Tabs(tabs = [navigation_panel, console_panel, export_panel])
        visualization = self.session.visualization.layout
        return make_layout([visualization, self.session.streamline_tab, homepage_tabs], orientation = LayoutOrientation.horizontal)

    # def make_navigation_panel(self):
    #     return make_layout([
    #         self.session.streamline_panel.navigation.prereq_plot.title, 
    #         self.session.streamline_panel.navigation.prereq_plot.p,
    #         self.session.streamline_panel.navigation.res_plot.title,
    #         self.session.streamline_panel.navigation.res_plot.p,
    #         self.session.streamline_panel.navigation.tracker.plot])

    def view_panel(self):
        curdoc().add_root(self.layout)