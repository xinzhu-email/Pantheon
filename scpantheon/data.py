import scanpy as sc
import os
import pandas as pd
import numpy as np
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

def init_data(adata: sc.AnnData,):
    if not isinstance(adata.X, np.ndarray): # judge dense matrix
        adata.uns["is_dense"] = False
    else:
        adata.uns["is_dense"] = True
    if adata.uns["is_dense"] is True:
        judge = adata.X[:, 0]
    else:
        judge = adata.X[:, 0].toarray().flatten()
    if np.isclose(judge.shape[0], np.trunc(judge)).all():
        adata.uns["original_log"] = False
    else: 
        adata.uns["original_log"] = True
    adata.obs = pd.DataFrame(
        index = adata.obs_names,
        columns = ['color', 'Please create a group']
    )
    adata.obs['color'] = color_list[0]
    adata.obs['Please create a group'] = 'unassigned'
    adata.uns['group_dict'] = dict()
    init_uns(adata, 'Please create a group', default = True)

def init_uns(
    adata: sc.AnnData,
    group_name: str,
    default: bool | None = None,
):
    empty_group_uns = pd.DataFrame(
        index = ['unassigned'],
        columns = ['color', 'cell_num']
    )
    empty_group_uns.loc['unassigned', 'cell_num'] = adata.n_obs
    if default:
        empty_group_uns.loc['unassigned', 'color'] = color_list[0]
    else:
        empty_group_uns.loc['unassigned', 'color'] = color_list[18]
    empty_group_uns.index = empty_group_uns.index.astype('category')
    adata.uns['group_dict'][group_name] = empty_group_uns
    adata.obs[group_name] = 'unassigned'

def update_uns_by_obs(
    adata: sc.AnnData,
    group_name: str | None = None,
    # color: str | None = None
):
    """
    cases to call: 
    when a cluster is created, obs is updated first
    """
    cluster_counts_series = pd.Series(adata.obs[group_name].value_counts())
    adata.uns['group_dict'][group_name]['cell_num'] = adata.uns['group_dict'][group_name]['cell_num'].index.map(cluster_counts_series).fillna(0).astype(int)

adata = None
