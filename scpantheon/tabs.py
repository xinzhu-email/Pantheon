from bokeh.layouts import column
from bokeh.models import Panel, Tabs
from bokeh.io import curdoc
import scanpy as sc
import os
from scpantheon.front_end.data_qt import dir, read_path


def load_adata():
    data_path = read_path(dir)[1]
    filetype = os.path.splitext(data_path)[-1]
    if filetype == '.csv':
        adata = sc.read_csv(data_path) 
        print('csv data')
    elif filetype == '.h5ad':
        adata = sc.read_h5ad(data_path)
        print('h5ad data')
    elif filetype == '': # not tested
        print("read_10x")
        adata = sc.read_10x_mtx(
            data_path,# the directory with the `.mtx` file
            var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
            cache=True)                              # write a cache file for faster subsequent reading
    else:
        print("error input")
    return adata


def view_panel(
    panel_dict,
    ext_layout,
    curpanel
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
adata = load_adata()
data = dict()
data['a'] = adata