import scanpy as sc
import os
import pandas as pd
from bokeh.palettes import d3

from scpantheon.front_end.data_qt import dir, read_path

color_list = d3['Category20c'][20]

def load_path():
    data_path = read_path(dir)[1]
    filetype = os.path.splitext(data_path)[-1]
    if filetype == '.csv':
        adata = sc.read_csv(data_path) 
        print('csv data')
        return adata
    elif filetype == '.h5ad':
        adata = sc.read_h5ad(data_path)
        print('h5ad data')
        return adata
    elif filetype == '': # not tested
        print("read_10x")
        adata = sc.read_10x_mtx(
            data_path,# the directory with the `.mtx` file
            var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
            cache=True)                              # write a cache file for faster subsequent reading
        return adata   
    else:
        print("error input")

def init_data(adata):
    adata.obs = pd.DataFrame(
        index = adata.obs_names,
        columns = ['color', 'default']
    )
    adata.obs['color'] = color_list[0]
    adata.obs['default'] = color_list[0]

adata = load_path()
init_data(adata)