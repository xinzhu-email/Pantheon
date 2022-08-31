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
        sc_pp_step0 = Button(label='Step0: Show gene percentage', button_type='primary')
        sc_pp_step0.on_click(show_gene_percentage)
        input1 =  TextInput(title='Min genes counts:',value='200')
        input2 =  TextInput(title='Min cells counts:',value='3')
        sc_pp_step1 = Button(label='Step1: Basic filter of genes and cells', button_type='primary')
        sc_pp_step1.on_click(lambda: basic_filter_callback(input1, input2))
        sc_pp_step2 = Button(label='Step2: Show violin plot of quality measures and scatter of total counts', button_type='primary')
        sc_pp_step2.on_click(mitochondrial_genes)
        input3 =  TextInput(title='Max total counts: ',value='2500')
        input4 =  TextInput(title='Max percentage of mitochondrial genes counts:',value='5')
        input5 =  TextInput(title='Target counts of normalization',value='1e5')
        sc_pp_step3 = Button(label='Step3: Filter cells with counts and mitochondrial, and total normalization and logarithmize', button_type='primary')
        sc_pp_step3.on_click(lambda: filter_norm_log(input3.value, input4.value, input5.value))
        input6 =  TextInput(title='Min mean expression of genes: ',value='0.0125')
        input7 =  TextInput(title='Max mean expression of genes: ',value='3')
        input8 =  TextInput(title='Min dispersions of genes',value='0.5')
        sc_pp_step4 = Button(label='Step4: Indentify highly variable genes', button_type='primary')
        sc_pp_step4.on_click(lambda: hvg(input6.value, input7.value, input8.value))

        self.scanpy_functions = column(sc_pp_step0,
                                       column(row(input1, input2),sc_pp_step1),
                                       sc_pp_step2,
                                       column(row(input3, input4, input5),sc_pp_step3),
                                       column(row(input6, input7, input8),sc_pp_step4))
        # self.scanpy_functions.name = 'Preprocessing_with_Scanpy'

    def add(self):
        return self.scanpy_functions


def show_gene_percentage():
    layout = curdoc().get_model_by_name('Preprocessing_with_Scanpy')
    change = connection()
    adata = change.get_anndata()
    figure = sc.pl.highest_expr_genes(adata, n_top=20, show=False )
    buf = BytesIO()
    figure.get_figure().savefig(buf, format="png")
    output1 = base64.b64encode(buf.getbuffer()).decode("ascii")
    div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output1))
    layout.children.append(div)

def basic_filter_callback(input1, input2):
    change = connection()
    adata = change.get_anndata()
    sc.pp.filter_cells(adata, min_genes=int(input1.value))
    sc.pp.filter_genes(adata, min_cells=int(input2.value))
    cells = list(adata.obs.index)    
    raw_adata = connection().get_anndata()    
    indices = raw_adata.obs[raw_adata.obs.index.isin(cells)]['ind']
    
    data_dict = json.loads(change.get_attributes())
    indices = list(set(indices)&set(data_dict['showing_indices']))
    data_dict['showing_indices'] = list(indices)
    change.set_attributes(data_dict)
    change.set_anndata(adata)

def mitochondrial_genes():
    layout = curdoc().get_model_by_name('Preprocessing_with_Scanpy')
    change = connection()
    adata = change.get_anndata()

    adata.var['mt'] = adata.var_names.str.startswith('MT-')
    sc.pp.calculate_qc_metrics(adata, qc_vars=['mt'], percent_top=None, log1p=False, inplace=True)
    print(adata.obs['pct_counts_mt'])
    figure1 = sc.pl.violin(adata, ['n_genes_by_counts', 'total_counts', 'pct_counts_mt'], jitter=0.4, multi_panel=True, show=False)
    figure2 = sc.pl.scatter(adata, x='total_counts', y='pct_counts_mt', show=False)
    figure3 = sc.pl.scatter(adata, x='total_counts', y='n_genes_by_counts', show=False)

    buf1, buf2, buf3 = BytesIO(), BytesIO(), BytesIO()
    figure1.savefig(buf1, format="png")
    output1 = base64.b64encode(buf1.getbuffer()).decode("ascii")
    div1 = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output1))
    layout.children.append(div1)
    figure2.get_figure().savefig(buf2, format="png")
    output2 = base64.b64encode(buf2.getbuffer()).decode("ascii")
    div2 = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output2))
    layout.children.append(div2)
    figure3.get_figure().savefig(buf3, format="png")
    output3 = base64.b64encode(buf3.getbuffer()).decode("ascii")
    div3 = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output3))    
    layout.children.append(div3)
    change.set_anndata(adata)

def filter_norm_log(gene_counts, mt_pct, target_sum):
    layout = curdoc().get_model_by_name('Preprocessing_with_Scanpy')
    change = connection()
    adata = change.get_anndata()

    adata = adata[adata.obs.n_genes_by_counts < float(gene_counts), :]
    adata = adata[adata.obs.pct_counts_mt < float(mt_pct), :]
    sc.pp.normalize_total(adata, target_sum=float(target_sum))
    sc.pp.log1p(adata)
    
    div1 = Div(text='<b>Cells are filtered with max counts of genes and max percentage of mitochondrial genes.<br/>Data is normalized and logarithmize.</b>')
    layout.children.append(div1)
    change.set_anndata(adata)

def hvg(min_mean, max_mean, min_disp):
    layout = curdoc().get_model_by_name('Preprocessing_with_Scanpy')
    change = connection()
    adata = change.get_anndata()

    sc.pp.highly_variable_genes(adata, min_mean=float(min_mean), max_mean=float(max_mean), min_disp=float(min_disp))
    figure = sc.pl.highly_variable_genes(adata, show=False)

    buf = BytesIO()
    figure.figure.savefig(buf, format="png")
    output1 = base64.b64encode(buf.getbuffer()).decode("ascii")
    div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output1))
    layout.children.append(div)



