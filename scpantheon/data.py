import scanpy as sc
import os
import pandas as pd
import numpy as np
from bokeh.palettes import d3
from scipy.sparse import csr_matrix
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

def init_data(
        adata: sc.AnnData,
        obsm_only: str | None = None
    ):
    """
    Initialize or format data for the application.

    :param adata: The AnnData object to initialize, namely dt.adata in extension modules.
    :type adata: AnnData
    :param obsm_only: The specific obsm key to initialize. Defaults to None. If obsm_only is the name of an obsm, the function only updates given obsm, or it updates all obsms.
    :type obsm_only: str | None
    :return: None
    :rtype: None
    """
    if not obsm_only:
        adata.uns['sparse'] = []
        if type(adata.X) == csr_matrix:
            judge = adata.X[:, 0].toarray().flatten()
            adata.uns['sparse'].append('X') # require: X reserved for obsm name
        else:
            judge = adata.X[:, 0]
        if np.isclose(judge.shape[0], np.trunc(judge)).all():
            adata.uns["original_log"] = False
        else: 
            adata.uns["original_log"] = True
    if adata.obsm.keys():
        update_data_obsm(adata, obsm_only)
    if adata.obs.empty: # reserved column names: 'color', 'Please create a group'
        adata.obs = pd.DataFrame(
            index = adata.obs_names,
            columns = ['color', 'Please create a group']
        )
    adata.obs['color'] = pd.Categorical(
        list(np.full(adata.n_obs, color_list[0])),
        categories = color_list, 
        ordered = True
    )
    adata.obs['Please create a group'] = pd.Categorical(
        list(np.full(adata.n_obs, 'unassigned')), 
        categories = ['unassigned'], 
        ordered = True
    )
    adata.obs = adata.obs.apply(lambda x: x.astype('category'))
    adata.uns['group_dict'] = dict()
    init_uns(adata, 'Please create a group', True)
    update_uns_all(adata)
    

def init_uns(
    adata: sc.AnnData,
    group_name: str | None = 'Please create a group',
    default: bool | None = None
):
    empty_group_uns = pd.DataFrame(
        index = ['unassigned'],
        columns = ['color', 'cell_num']
    )
    empty_group_uns['color'] = pd.Categorical(
        ['unassigned'],
        categories = color_list,
        ordered = True
    )
    empty_group_uns['cell_num'] = pd.Categorical(
        [adata.n_obs],
        categories = [adata.n_obs],
        ordered = True
    )
    if adata.n_obs not in empty_group_uns['cell_num'].cat.categories:
        empty_group_uns['cell_num'] = empty_group_uns['cell_num'].cat.add_categories([adata.n_obs])
    empty_group_uns.loc['unassigned', 'cell_num'] = adata.n_obs
    if color_list[0] not in empty_group_uns['color'].cat.categories:
        empty_group_uns['color'] = empty_group_uns['color'].cat.add_categories([color_list[0]])
    if color_list[18] not in empty_group_uns['color'].cat.categories:
        empty_group_uns['color'] = empty_group_uns['color'].cat.add_categories([color_list[18]])
    if default:
        empty_group_uns.loc['unassigned', 'color'] = color_list[0]
    else:
        empty_group_uns.loc['unassigned', 'color'] = color_list[18]
    empty_group_uns.index = empty_group_uns.index.astype('category')
    adata.uns['group_dict'][group_name] = empty_group_uns
    if group_name not in adata.obs.columns:
        adata.obs[group_name] = pd.Categorical(
            list(np.full(adata.n_obs, 'unassigned')), 
            categories = ['unassigned'], 
            ordered = True
        )

def update_data_obsm(
    adata: sc.AnnData,
    obsm_key: str | None = None    
):
    if not obsm_key:
        for obsm_key in adata.obsm_keys():
            if type(adata.obsm[obsm_key]) == csr_matrix:
                adata.uns['sparse'].append(obsm_key)
            if type(adata.obsm[obsm_key]) == np.ndarray:
                column_names = list([obsm_key + str(i) for i in range(adata.obsm[obsm_key].shape[1])])
                adata.obsm[obsm_key] = pd.DataFrame(
                    adata.obsm[obsm_key],
                    index = adata.obs_names,
                    columns = column_names
                )
    else:
        if obsm_key not in adata.obsm_keys():
            print("Warning: no obsm", obsm_key)
            return
        if type(adata.obsm[obsm_key]) == csr_matrix:
            adata.uns['sparse'].append(obsm_key)
        if type(adata.obsm[obsm_key]) == np.ndarray:
            column_names = list([obsm_key + str(i) for i in range(adata.obsm[obsm_key].shape[1])])
            adata.obsm[obsm_key] = pd.DataFrame(
                adata.obsm[obsm_key],
                index = adata.obs_names,
                columns = column_names
            )


def update_uns_all(
    adata: sc.AnnData,
):
    """
    cases to call: 
    when a cluster is created, obs is updated first, uns cluster not defined
    """
    for group_name in adata.obs_keys():
        if group_name != 'color' and group_name != 'Please create a group':
            if group_name not in adata.uns['group_dict'].keys():
                init_uns(adata, group_name)
            update_uns_hybrid_obs(adata, group_name)

def update_uns_hybrid_obs(
    adata: sc.AnnData,
    group_name: str | None = None,
    mode: str | None = 'merge'
):
    """
    cases to call: 
    when a cluster is created, obs is updated first, uns cluster not defined
    """
    cluster_counts_series = pd.Series(adata.obs[group_name].value_counts())
    clusterlist_obs = cluster_counts_series.index.tolist()
    clusterlist_uns = adata.uns['group_dict'][group_name].index.tolist()
    clusterlist = list(set(clusterlist_uns+ clusterlist_obs))
    if mode == 'merge':
        adata.uns['group_dict'][group_name] = adata.uns['group_dict'][group_name].reindex(clusterlist)
        clusterlist = adata.uns['group_dict'][group_name].index.tolist()
        adata.uns['group_dict'][group_name]['cell_num'] = adata.uns['group_dict'][group_name]['cell_num'].index.map(cluster_counts_series).fillna(0).astype(int)
        for clustername in clusterlist:
            if pd.isna(adata.uns['group_dict'][group_name].loc[clustername, 'color']):
                curcolor = color_list[(clusterlist.index(clustername))%20]
                if curcolor not in adata.uns['group_dict'][group_name]['color'].cat.categories:
                    adata.uns['group_dict'][group_name]['color'] = adata.uns['group_dict'][group_name]['color'].cat.add_categories([curcolor])
                adata.uns['group_dict'][group_name].loc[clustername,'color'] = curcolor
    elif mode == 'uns':
        uns_clusterlist = adata.uns['group_dict'][group_name].index
        adata.uns['group_dict'][group_name] = adata.uns['group_dict'][group_name].reindex(clusterlist)
        clusterlist = adata.uns['group_dict'][group_name].index.tolist()
        adata.uns['group_dict'][group_name]['cell_num'] = adata.uns['group_dict'][group_name]['cell_num'].index.map(cluster_counts_series).fillna(0).astype(int)
        for clustername in clusterlist:
            if clustername not in uns_clusterlist:
                adata.uns['group_dict'][group_name] = adata.uns['group_dict'][group_name].drop(clustername)
    if adata.uns['group_dict'][group_name]['color'].dtype != 'category':
        adata.uns['group_dict'][group_name]['color'] = pd.Categorical(adata.uns['group_dict'][group_name]['color'])
    if adata.uns['group_dict'][group_name]['cell_num'].dtype != 'category':
        adata.uns['group_dict'][group_name]['cell_num'] = pd.Categorical(adata.uns['group_dict'][group_name]['cell_num'])

adata = None
