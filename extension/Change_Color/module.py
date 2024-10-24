<<<<<<< HEAD
from bokeh.models import Button
import json
import sys
from pathlib import Path
from bokeh.io import curdoc

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scpantheon import source as soc

class new_layout:
    def __init__(self):
        self.new_button = Button(label='Change Color')
        self.new_button.on_click(change_color) 
    
    def add(self):
        return self.new_button
    

def button_disabled(buttons_group):
    for b in buttons_group:
        b.disabled = True

def button_abled(buttons_group):
    for b in buttons_group:
        b.disabled = False


def change_color(): 
    global buttons_group

    plot = soc.plot_function()
    buttons_group, b = plot.get_buttons_group()
    button_disabled(buttons_group)
    def next_color(buttons_group):
        soc.plot_function().show_checked()
        trans = soc.connection()
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
        soc.plot_function().change_checkbox_color()
        button_abled(buttons_group)
    curdoc().add_next_tick_callback(lambda : next_color(buttons_group))
=======
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[3]))
from bokeh.models import Div, Select, Button, CheckboxGroup, TextInput, ColorPicker, AutocompleteInput, ColumnDataSource
from bokeh.palettes import d3
from bokeh.layouts import row, column
from Pantheon.scpantheon.myplot import Plot
from Pantheon.scpantheon.widgets import Widgets
import data as dt
import numpy as np
import pandas as pd


class Widgets_Color(Widgets):
    def __init__(self,
        name: str | None = 'generic columns',
    ):
        """
        dt.adata: handle with anndata structure  
        .obs: a pd.Dataframe with cell names as index, color and group name as columns  
        denotes a certain cell's current visualized color and which cluster it belongs to in each group  
        .uns: a dict {map_name: {group_name : pd.Dataframe}}  
        pd.Dataframe's index are cluster names, columns are color and cell_num  
        denotes each cluster's color and cell number
        """
        self.update_data()
        super().__init__(name)
        super().init_tab()


    def update_data(self):
        my_obsm = np.zeros((dt.adata.n_obs, 2))
        dt.adata.obsm['cluster'] = my_obsm
        if dt.adata.obsm:
            for key in dt.adata.obsm_keys(): 
                if type(dt.adata.obsm[key]) == np.ndarray:
                    column_names = list([key + str(i) for i in range(dt.adata.obsm[key].shape[1])])
                    dt.adata.obsm[key] = pd.DataFrame(
                        dt.adata.obsm[key],
                        index = dt.adata.obs_names,
                        columns = column_names
                    )
>>>>>>> extension
