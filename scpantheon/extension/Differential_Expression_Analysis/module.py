import os
from pickletools import optimize
import scanpy as sc
from io import BytesIO
from bokeh.palettes import d3
import json
import base64
import sys
from pathlib import Path
from bokeh.io import curdoc
from bokeh.models import FileInput, Button, TextInput, Div, Select, MultiChoice
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
            # to_json = api.get_attributes()
            # data_dict = json.loads(to_json)
            # group = data_dict['selected_group']            
            # cluster_list = list(api.get_group_dict()[group]['class_name'])
            total_gene = list(api.get_anndata().var_names)
        except:
            print('No Group!')
        method = Select(title='Select method:', options=['wilcoxon','t-test', 'logreg'], value='t-test')
        gene_num = TextInput(title='Input gene nums to show:', value='20')
        rank_genes = Button(label='Compare gene expression to a single cluster', button_type='success')
        rank_genes.on_click(lambda: rank(method=method.value,gene_num=int(gene_num.value)))
        violin_figure = Button(label='Show violin plot', button_type='success')
        violin_figure.on_click(lambda: violin(gene_num=int(gene_num.value)))
        
        gene_list = MultiChoice(title='Choose genes:',options=total_gene, value=[''])
        certain_gene = Button(label='Compare genes acros clusters', button_type='success')
        certain_gene.on_click(lambda: compare(gene_list=gene_list.value,group=group))

        self.de = column(row(method,gene_num),rank_genes,violin_figure,gene_list,certain_gene)

    def add(self):
        return self.de



def get_attr():
    api = connection()
    to_json = api.get_attributes()
    data_dict = json.loads(to_json)
    group = data_dict['selected_group']
    cluster_list = api.get_group_dict()[group]
    return group, cluster_list


def rank(method,gene_num):
    layout = curdoc().get_model_by_name('Differential_Expression_Analysis')
    api = connection()
    to_json = api.get_attributes()
    data_dict = json.loads(to_json)
    group = data_dict['selected_group']
    cluster_list = list(api.get_group_dict()[group]['class_name'])
    adata = api.get_anndata()
    print(cluster_list)
    sc.tl.rank_genes_groups(adata, group, groups=cluster_list[1:], reference=cluster_list[0], method=method)
    sc.pl.rank_genes_groups(adata, groups=cluster_list[1:], n_genes=gene_num, save='.png')

    name = 'figures/rank_genes_groups_' + group + '.png'
    img = open(name,'rb')
    img_base64 = base64.b64encode(img.read()).decode("ascii")
    div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
    layout.children.append(div)
    api.set_uns(adata.uns)


def violin(gene_num):
    layout = curdoc().get_model_by_name('Differential_Expression_Analysis')
    api = connection()
    to_json = api.get_attributes()
    data_dict = json.loads(to_json)
    group = data_dict['selected_group']
    cluster_list = list(api.get_group_dict()[group]['class_name'])
    adata = api.get_anndata()

    sc.pl.rank_genes_groups_violin(adata, groups=cluster_list[1:], n_genes=gene_num, save='.png')

    for cluster in cluster_list[1:]:
        name = 'figures/rank_genes_groups_' + group + '_' + cluster + '.png'
        img = open(name,'rb')
        img_base64 = base64.b64encode(img.read()).decode("ascii")
        div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
        layout.children.append(div)

def compare(gene_list,group):
    layout = curdoc().get_model_by_name('Differential_Expression_Analysis')
    api = connection()

    adata = api.get_anndata()

    sc.pl.violin(adata, gene_list, groupby=group, save='.png')

    img = open('figures/violin.png','rb')
    img_base64 = base64.b64encode(img.read()).decode("ascii")
    div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
    layout.children.append(div)