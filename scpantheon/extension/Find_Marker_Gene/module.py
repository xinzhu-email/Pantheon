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
try:
    from scpantheon.source import connection, plot_function
except:
    from source import connection, plot_function

color_list = d3['Category20c'][20]

class new_layout:
    def __init__(self):
        try:
            group, cluster_list = get_attr()
            api = connection()
            to_json = api.get_attributes()
            data_dict = json.loads(to_json)
            group = data_dict['selected_group']            
            cluster_list = list(api.get_group_dict()[group]['class_name'])
        except:
            print('No Group!')

        test_method = Select(title='Choose the method:', options=['t-test','wilcoxon','logreg'], value='t-test')
        rank_n_genes = TextInput(title='Input the num of genes to rank')
        marker = Button(label='Find marker of these clusters', button_type='success')
        marker.on_click(lambda: find_marker(groupby=group, test_method=test_method.value, rank_n_genes=int(rank_n_genes.value)))
        violin_figure = Button(label='Show violin plot', button_type='success')
        violin_figure.on_click(lambda: violin(cluster_list=cluster_list, gene_num=int(rank_n_genes.value)))

        self.marker = column(row(test_method, rank_n_genes),marker,violin_figure)
        # self.marker.name = 'Find_Marker_Gene'

    def add(self):
        return self.marker


def get_attr():
    api = connection()
    to_json = api.get_attributes()
    data_dict = json.loads(to_json)
    group = data_dict['selected_group']
    cluster_list = api.get_group_dict()[group]
    return group, cluster_list

def find_marker(groupby='leiden',test_method='t-test',rank_n_genes=25):
    layout = curdoc().get_model_by_name('Find_Marker_Gene')
    change = connection()
    adata = change.get_anndata()

    sc.tl.rank_genes_groups(adata, groupby, method=test_method)
    sc.pl.rank_genes_groups(adata, n_genes=rank_n_genes, sharey=False, save='.png')

    name = 'figures/rank_genes_groups_' + groupby + '.png'
    img = open(name,'rb')
    img_base64 = base64.b64encode(img.read()).decode("ascii")
    div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
    layout.children.append(div)
    change.set_obsm(adata.obsm)

def violin(cluster_list,gene_num):
    layout = curdoc().get_model_by_name('Find_Marker_Gene')
    api = connection()
    adata = api.get_anndata()

    sc.pl.rank_genes_groups_violin(adata, groups=cluster_list[1:], n_genes=gene_num, save='.png')

    img = open('figures/violin.png','rb')
    img_base64 = base64.b64encode(img.read()).decode("ascii")
    div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
    layout.children.append(div)