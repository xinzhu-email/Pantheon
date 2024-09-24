from bokeh.layouts import column
from bokeh.models import Panel, Tabs
from bokeh.io import curdoc
from scpantheon.front_end.data_qt import dir, read_path

def view_panel(
    panel_dict,
    ext_layout,
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
    curdoc().add_root(panel_view)


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


panel_dict = dict()
curpanel = None
ext_layout = column([])