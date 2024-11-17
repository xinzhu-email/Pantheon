import scanpy as sc
import os
import sys
from pathlib import Path
import pandas as pd
import numpy as np
from bokeh.palettes import d3
from scipy.sparse import csr_matrix
sys.path.append(str(Path(__file__).resolve().parents[1]))
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
        adata: sc.AnnData
    ):
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
        update_data_obsm(adata)
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
    group_name: str,
    default: bool | None = None
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
    if group_name not in adata.obs.columns:
        adata.obs['Please create a group'] = pd.Categorical(
            list(np.full(adata.n_obs, 'unassigned')), 
            categories = ['unassigned'], 
            ordered = True
        )

def update_data_obsm(
    adata: sc.AnnData    
):
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
                adata.uns['group_dict'][group_name].loc[clustername,'color'] = color_list[(18 + clusterlist.index(clustername))%20]
    elif mode == 'uns':
        uns_clusterlist = adata.uns['group_dict'][group_name].index
        adata.uns['group_dict'][group_name] = adata.uns['group_dict'][group_name].reindex(clusterlist)
        clusterlist = adata.uns['group_dict'][group_name].index.tolist()
        adata.uns['group_dict'][group_name]['cell_num'] = adata.uns['group_dict'][group_name]['cell_num'].index.map(cluster_counts_series).fillna(0).astype(int)
        for clustername in clusterlist:
            if clustername not in uns_clusterlist:
                adata.uns['group_dict'][group_name] = adata.uns['group_dict'][group_name].drop(clustername)

adata = None
# adata = load_path()
# print(adata.obs)
# sc.tl.pca(adata, svd_solver='arpack')
# init_data(adata)
# print(adata.obsm['X_pca'])
# X = adata.obsm["X_pca"].to_numpy()[:, :4]
# print(adata.obsm['X_pca'])
# print(X)
# """
# [[-2.7944040e+00 -9.1026878e-01  1.2102165e+00 ... -3.0550727e-01
#   -2.0245600e-01  4.1821671e-01]
#  [ 3.0735812e-01  4.4000139e+00 -1.8132286e+00 ...  9.3825227e-01
#   -8.0293655e-02  5.6981939e-01]
#  [-2.6968875e+00 -1.7179914e+00 -2.8975086e+00 ... -5.5406791e-01
#   -7.6532841e-02 -6.3562497e-02]
#  ...
#  [-1.3689178e+00 -1.4851947e+00 -2.9930458e+00 ...  1.2974060e-01
#    3.0403605e-01  1.0140352e+00]
#  [-1.9800688e+00  3.3172290e+00 -3.4132576e-01 ... -5.4733843e-01
#    5.9092045e-04 -2.5331450e-01]
#  [-4.5481563e-02  4.4525657e+00 -2.0641232e-01 ...  2.3479615e-01
#    1.4979887e-01 -3.1675580e-01]]
# """

'''
                                   X_pca0       X_pca1       X_pca2  ...    X_pca10     X_pca11    X_pca12
BMMC_D1T1:AAACCCAAGATGCAGC-1 -2662.330322  3447.128418   -58.011433  ...  -3.601589  -25.462214 -41.821831
BMMC_D1T1:AAACCCACAAACTCGT-1  -596.927490 -1761.758545  -806.322754  ...   2.987983    4.182689   3.766137
BMMC_D1T1:AAACCCACAGTGTACT-1  -655.122070 -1803.200684 -1012.829102  ...   5.868218  -21.308332  -6.196320
BMMC_D1T1:AAACCCATCGCTATTT-1   500.916046  1608.081787  3186.302002  ...   5.614631   26.496035  34.240807
BMMC_D1T1:AAACGAACACCCAATA-1  -395.295349 -1944.190674  -493.124451  ... -19.528751    7.531777  -5.799384
...                                   ...          ...          ...  ...        ...         ...        ...
BMMC_D1T1:TTTGTTGAGCGAGTCA-1  -848.593384   669.082947   788.681335  ...   6.666115   70.325584 -21.808229
BMMC_D1T1:TTTGTTGGTGCAACAG-1  2108.062988 -1796.340820  3553.788330  ... -64.586494  -28.835665  -8.045574
BMMC_D1T1:TTTGTTGGTGTTACAC-1  1793.939453 -1843.930542  3134.898926  ... -55.301994   -9.103964   1.273581
BMMC_D1T1:TTTGTTGTCTAGTCAG-1  -712.409973 -1834.821289 -1000.610291  ... -10.446795   -0.266144  10.146390
BMMC_D1T1:TTTGTTGTCTTGGTGA-1 -1745.229858   636.920105  -560.861450  ...  -5.170202  121.677071 -30.855532
'''

'''
                      X_pca0    X_pca1    X_pca2    X_pca3  ...   X_pca46   X_pca47   X_pca48   X_pca49
AAACAAGTATCTCCCA-1 -2.794404 -0.910269  1.210217 -1.555550  ... -0.048031 -0.305507 -0.202456  0.418217
AAACAATCTACTAGCA-1  0.307358  4.400014 -1.813229  1.239908  ... -0.200442  0.938252 -0.080294  0.569819
AAACACCAATAACTGC-1 -2.696887 -1.717991 -2.897509 -2.005396  ... -0.289838 -0.554068 -0.076533 -0.063562
AAACAGAGCGACTCCT-1  3.339939  0.986992 -2.202252  0.990381  ... -0.278483  1.067402  0.140830 -0.184259
AAACAGCTTTCAGAAG-1  2.956325 -1.231612  0.610858  3.007709  ... -0.205753  0.017049 -0.203935  0.117980
...                      ...       ...       ...       ...  ...       ...       ...       ...       ...
TTGTTTCACATCCAGG-1 -2.958202 -1.553407 -0.718594 -0.610992  ...  0.387912 -0.225467 -0.286943  1.227487
TTGTTTCATTAGTCTA-1 -1.697715 -1.993960 -3.013733 -0.343296  ...  0.073724 -1.746935  0.261613  0.571816
TTGTTTCCATACAACT-1 -1.368918 -1.485195 -2.993046 -0.557790  ...  1.652696  0.129741  0.304036  1.014035
TTGTTTGTATTACACG-1 -1.980069  3.317229 -0.341326  1.442389  ...  1.441427 -0.547338  0.000591 -0.253314
TTGTTTGTGTAAATTC-1 -0.045482  4.452566 -0.206412  0.509220  ...  0.193197  0.234796  0.149799 -0.316756
'''