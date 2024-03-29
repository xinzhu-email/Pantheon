import os
import scanpy as sc
from io import BytesIO
from bokeh.palettes import d3
import json
import base64
import sys
from pathlib import Path
from bokeh.io import curdoc
from bokeh.models import FileInput, Button, TextInput, Div, Select
from bokeh.layouts import row, column

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scpantheon import source as soc

color_list = d3['Category20c'][20]


class new_layout:
    def __init__(self):
        sc_cluster_step1 = Button(label='Step1: Run PCA', button_type='success')
        sc_cluster_step1.on_click(pca)
        cl_input1 = TextInput(title='Neighbor Num:', value='10')
        cl_input2 = TextInput(title='Principal Component Num:', value='40')
        cl_input3 = TextInput(title='Resolution', value='1')
        sc_cluster_step2 = Button(label='Step2: Clustering with Neighborhood Graph', button_type='success')
        sc_cluster_step2.on_click(lambda: neighborhood_graph(cl_input1.value, cl_input2.value, cl_input3.value))
        
        # layout format changed: delete the inner column
        self.scanpy_cluster = column(sc_cluster_step1,
                                     row(cl_input1, cl_input2 ,cl_input3),
                                     sc_cluster_step2)
        # self.scanpy_cluster.name = 'Clustering_with_Scanpy'

    def add(self):
        return self.scanpy_cluster


def button_disabled(buttons_group):
    for b in buttons_group:
        b.disabled = True

def button_abled(buttons_group):
    for b in buttons_group:
        b.disabled = False
    

def pca():
    global buttons_group
    plot = soc.plot_function()
    buttons_group, b = plot.get_buttons_group()
    button_disabled(buttons_group)
    def next_pca(buttons_group):
        '''for b in buttons_group:
            print(b.disabled)'''
        layout = curdoc().get_model_by_name('Clustering_with_Scanpy')
        change = soc.connection()
        adata = change.get_anndata()

        sc.tl.pca(adata, svd_solver='arpack')
        sc.pl.pca_variance_ratio(adata, log=True, save='.png')

        img = open('figures/pca_variance_ratio.png','rb')
        img_base64 = base64.b64encode(img.read()).decode("ascii")
        div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
        layout.children.append(div)
        change.set_obsm(adata.obsm)
        # change.set_anndata(adata)
        button_abled(buttons_group)
    curdoc().add_next_tick_callback(lambda : next_pca(buttons_group))

def neighborhood_graph(neighbor_num, pc_num, resolution):
    button_disabled(buttons_group)
    def next_neighbor(buttons_group, neighbor_num, pc_num, resolution):
        layout = curdoc().get_model_by_name('Clustering_with_Scanpy')
        change = soc.connection()
        adata = change.get_anndata()

        adata = sc.pp.neighbors(adata, n_neighbors=int(neighbor_num), n_pcs=int(pc_num), copy=True)
        sc.tl.umap(adata)
        sc.tl.leiden(adata, resolution=float(resolution))
        print('new')

        change.set_obsm(adata.obsm)
        change.set_uns(adata.uns)
        change.set_obs(adata.obs, set_group_name=['leiden'])
        button_abled(buttons_group)
    curdoc().add_next_tick_callback(lambda : next_neighbor(buttons_group, neighbor_num, pc_num, resolution))