#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  7 18:59:08 2022

@author: lianqiuyu
"""


import scanpy as sc
import pickle
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns


def display_subdata(data,node_data,**para):
    
    savepath = para.get('savepath',None)
    dpi = para.get('dpi',64)
    hist_bw = para.get('hist_bw',0.2)
    fig_name = para.get('fig_name',None)

    if savepath is not None and fig_name is None:
        print('Warning: Para fig_name is required to save figures.')
        return
    
    #print('plot histgrams of all markers in CLR format.')
    plt.figure(figsize=(12,2*np.ceil(node_data.shape[1] / 5)), dpi=dpi)
    plt.style.use('seaborn-white')
    for i in range(node_data.shape[1]):
        ax = plt.subplot(int(np.ceil(node_data.shape[1] / 5)),5,i+1)
        sns.distplot(data.iloc[:,i].values,kde_kws={'bw':0.2},color='gray')
        sns.distplot(node_data.iloc[:,i].values,kde_kws={'bw':hist_bw},color='red')
        plt.yticks([0,1])
        plt.title(node_data.columns[i],fontsize=15)
        if i%5 == 0:
            plt.ylabel('Density',fontsize=12)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.yaxis.set_ticks_position('left')
    
    if fig_name is None:
        plt.suptitle(str(node_data.shape[0])+' droplets',fontsize=18)  
    else:
        plt.suptitle(fig_name+', '+str(node_data.shape[0])+' droplets',fontsize=18)    
        
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.6,wspace=0.15)
    plt.subplots_adjust(top=0.8)
    if savepath is not None:
        plt.savefig(savepath+'/'+fig_name.replace(' ','_')+'.png')
    plt.show()
    #plt.show()
    
        
#%%

ct_layer = 'celltype.l2'
# data = pd.read_csv('./public_data/BM_seuratv3_CITEsort/data_clr.csv',header=0,index_col=0)
data = pd.read_csv('./data/SeuratV4/adt_clr.csv',header=0,index_col=0)
# data = pd.read_csv('./data/SeuratV3_adt/clr_adt.csv',header=0,index_col=0)

# info = pd.read_csv('./UMI_distribution/info_UMI_celltypes/metadata_seuratV3.txt',sep='\t',header=0,index_col=0)
info = pd.read_csv('./data/SeuratV4/metadata_seuratV4.txt',sep='\t',header=0,index_col=0)
# info = pd.read_csv('./data/SeuratV3_adt/memory_B_metadata.csv',sep=',')
import anndata

# info = anndata.read('./data/SeuratV3_adt/CD56+CD3result.h5ad')
# info = pd.DataFrame(columns=[ct_layer],data=info.obs[ct_layer])

info.index = [x.replace('-','.') for x in list(info.index)]


combarcodes = list(set(data.index).intersection(info.index))



data = data.loc[combarcodes,:]
info = info.loc[combarcodes,:]


cell_types = info[ct_layer].unique()

for ct in cell_types:
    print(ct)
    subdata = data.loc[info.loc[info[ct_layer]==ct,:].index,:]
    # display_subdata(data, subdata, savepath='./public_data/BM_seuratv3_CITEsort/ADThist_seuratAnnotation',fig_name=ct,dpi=256)
    display_subdata(data, subdata, savepath='./data/SeuratV4_l2_ADT_hist_Annotation',fig_name=ct,dpi=256)
    # if ct == 'CD56 bright NK':
    #     display_subdata(data, subdata, savepath='./data/SeuratV3_ADT_hist_Annotation',fig_name=ct,dpi=256)





# from scipy.io import mmread
# import numpy as np
# import pandas as pd
# import scanpy as sc

# a = mmread('./Downloads/result1/umi_count/matrix.mtx')
# m = a.todense()
# m = np.transpose(m)

# barcodes = pd.read_csv('./Downloads/result1/umi_count/barcodes.tsv',sep='\t',header=None)

# hto = pd.DataFrame(m,index=barcodes.loc[:,0])

# hto.columns = ['Hashtag_'+str(i+1) for i in range(11)]
# hto.iloc[:,:-1].to_csv('./Downloads/result1/hto.csv')


# protein = sc.AnnData(hto)#.iloc[:,:-1])

# #sc.pp.normalize_geometric(protein)
# sc.pp.log1p(protein)
# sc.pp.pca(protein, n_comps=8)
# sc.pp.neighbors(protein, n_neighbors=30)  # why can't we just work with the default neighbors?
# sc.tl.leiden(protein, key_added="protein_leiden")
# # TODO: remove
# protein.obsp["protein_connectivities"] = protein.obsp["connectivities"].copy()
# sc.tl.umap(protein)
# sc.pl.umap(protein, color="protein_leiden", size=10)


# sc.pl.umap(protein,color=['Hashtag_'+str(i+1) for i in range(11)])

