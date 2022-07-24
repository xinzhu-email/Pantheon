from bokeh.io import curdoc
from bokeh.models import FileInput, Button, TextInput
from transform import data_trans
from bokeh.layouts import row, column
import anndata
import scanpy as sc
import json
from source import connection, plot_function

class new_layout:
    def __init__(self):
        self.new_button = Button(label='Change Color')
        self.new_button.on_click(change_color) 
        self.input =  TextInput(value='Input min genes expressed in cell')
        self.filter_button = Button(label='Filter the Cells')
        self.filter_button.on_click(lambda: filter_cells_callback(self.input))

    def add(self):
        options = [self.new_button, row(self.input, self.filter_button)]
        return options

    def options(self):
        return ['Change Color', 'Filter Cells with Gene Expression']


### Examples to add buttons ###
def change_color(): 
    plot_function().show_checked()
    trans = connection()
    to_json = trans.get_attributes()
    data_dict = json.loads(to_json)
    color = data_dict['selected_color']
    selected_class = data_dict['checked_class']
    group = data_dict['selected_group']
    group_dict = trans.get_group_dict()
    group_dict[group]['color'][[i for i in selected_class]] = color   
    trans.set_group_dict(group_dict)
    indices = data_dict['selected_indices']
    data_color = data_dict['data_color']
    for i in indices:
        data_color[i] = color
    # Save change of data into the Figure
    data_dict['data_color'] = data_color
    trans.set_attributes(data_dict)
    plot_function().change_checkbox_color()

def filter_cells_callback(input):
    change = connection()
    adata = change.get_anndata()
    sc.pp.filter_cells(adata, min_genes=int(input.value))
    cells = list(adata.obs.index)    
    raw_adata = connection().get_anndata()    
    indices = raw_adata.obs[raw_adata.obs.index.isin(cells)]['ind']
    
    data_dict = json.loads(change.get_attributes())
    indices = list(set(indices)&set(data_dict['showing_indices']))
    data_dict['showing_indices'] = list(indices)
    change.set_attributes(data_dict)





