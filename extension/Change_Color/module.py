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