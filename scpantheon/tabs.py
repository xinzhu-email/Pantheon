from bokeh.layouts import column
from bokeh.models import Panel, Tabs
from bokeh.io import curdoc

panel_dict = dict()
curpanel = None
ext_layout = column([])
ext_widgets = dict()

def view_panel(
    panel_dict,
    ext_layout,
    ext_widgets: dict,
    curpanel: str | None = None 
):
    curdoc().clear()
    tab_list = []
    for key in panel_dict:
        key_layout = panel_dict[key].layout
        panel_layout = ext_layout
        layout = column(key_layout, panel_layout)
        panel_creat = Panel (child = layout, title = key)
        tab_list.append (panel_creat)
    panel_view = Tabs(tabs = tab_list)
    panel_view.active = get_index(panel_dict, curpanel)
    panel_view.on_change('active',lambda attr, old, new : update_curpanel(panel_dict, curpanel, ext_widgets, attr, old, new))
    curdoc().add_root(panel_view)

def update_curpanel(panel_dict, curpanel, ext_widgets, attr, old, new):
    mute_global(panel_dict, curpanel, ext_widgets)
    def update_curpanel_next(panel_dict, curpanel, ext_widgets, new):
        key_list = list(panel_dict.keys())
        curpanel = key_list[new]
        print(curpanel)
        panel_dict[curpanel].switch_tab()
        unmute_global(panel_dict, curpanel, ext_widgets)
    curdoc().add_next_tick_callback(lambda: update_curpanel_next(panel_dict, curpanel, ext_widgets, new))

def get_index(
    panel_dict: dict | None = None,
    curpanel: str | None = None,
):
    key_list = list(panel_dict.keys())
    if curpanel in key_list:
        index_position = key_list.index(curpanel)
    else:
        index_position = 0
    return index_position

def mute_global(
    panel_dict: dict,
    curpanel: str,
    ext_widgets: dict
):
    Tabs.disabled = True
    if ext_widgets:
        for widget_key in ext_widgets:
            ext_widgets[widget_key].disabled = True
    if panel_dict:
        for widget_key in panel_dict[curpanel].widgets_dict:
            panel_dict[curpanel].widgets_dict[widget_key].disabled = True  
  
def unmute_global(
    panel_dict: dict,
    curpanel: str,
    ext_widgets: dict
):
    Tabs.disabled = False
    if ext_widgets:
        for widget_key in ext_widgets:
            ext_widgets[widget_key].disabled = False
    if panel_dict:
        for widget_key in panel_dict[curpanel].widgets_dict:
            panel_dict[curpanel].widgets_dict[widget_key].disabled = False