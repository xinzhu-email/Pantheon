from bokeh.io import curdoc
from bokeh.models import FileInput, Button, TextInput, Div, Select
from sklearn import cluster
from transform import data_trans
from bokeh.layouts import row, column
import anndata
import scanpy as sc
import json
from bokeh.palettes import d3

import tomas as tm
import scanpy as sc
import numpy as np
import pandas as pd
import base64
from io import BytesIO
import os


from source import connection, plot_function

color_list = d3['Category20c'][20]

class new_layout:
    def __init__(self):
        self.new_button = Button(label='Change Color')
        self.new_button.on_click(change_color) 

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
        self.scanpy_functions.name = 'scanpy_fucntions'


        sc_cluster_step1 = Button(label='Step1: Run PCA', button_type='success')
        sc_cluster_step1.on_click(pca)
        cl_input1 = TextInput(title='Neighbor Num:', value='10')
        cl_input2 = TextInput(title='Principal Component Num:', value='40')
        cl_input3 = TextInput(title='Resolution', value='1')
        sc_cluster_step2 = Button(label='Step2: Clustering with Neighborhood Graph', button_type='success')
        sc_cluster_step2.on_click(lambda: neighborhood_graph(cl_input1.value, cl_input2.value, cl_input3.value))
        
        
        self.scanpy_cluster = column(sc_cluster_step1,
                                     column(row(cl_input1, cl_input2 ,cl_input3),sc_cluster_step2))
        self.scanpy_cluster.name = 'scanpy_cluster'

        

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
        de_analysis = Button(label='Find marker of these clusters', button_type='success')
        de_analysis.on_click(lambda: find_marker(groupby=group, test_method=test_method.value, rank_n_genes=int(rank_n_genes.value)))
        self.marker = column(row(test_method, rank_n_genes),de_analysis)
        self.marker.name = 'find_marker'

        try:
            homo1_selection = Select(title='Homo-celltype1:', options=cluster_list, value=cluster_list[0], background=color_list[2])
            homo2_selection = Select(title='Homo-celltype2:', options=cluster_list, value=cluster_list[1], background=color_list[2])
            hetero_selection = Select(title='Hetero-doublet:', options=cluster_list, value=cluster_list[2], background=color_list[2])
            tomas_step1 = Button(label='Step1: Display UMI amount distribution')
            tomas_step1.on_click(lambda: tomas_callback1(group, [homo1_selection.value, homo2_selection.value, hetero_selection.value]))
            tomas_step2 = Button(label='Step2: Raw total UMI ratio')
            tomas_step2.on_click(lambda: tomas_callback2(group, [homo1_selection.value, homo2_selection.value, hetero_selection.value]))
            tomas_step3 = Button(label='Step3: Fit DMN model')
            tomas_step3.on_click(lambda: tomas_callback3(group, [homo1_selection.value, homo2_selection.value, hetero_selection.value]))
            tomas_step4 = Button(label='Step4: Merge genes into exclusive meta-gene')
            tomas_step4.on_click(lambda: tomas_callback4(group, [homo1_selection.value, homo2_selection.value, hetero_selection.value]))
            tomas_step5 = Button(label='Step5: Display the total UMI distribution')
            tomas_step5.on_click(lambda: tomas_callback5(group, [homo1_selection.value, homo2_selection.value, hetero_selection.value]))

            select_group = row(homo1_selection, homo2_selection, hetero_selection)
            self.tomas_layout = column(select_group, tomas_step1, tomas_step2, tomas_step3, tomas_step4, tomas_step5)
            self.tomas_layout.name = 'tomas_layout'
        except:
            self.tomas_layout = column()


    def add(self):
        options = [self.new_button, self.scanpy_functions, self.scanpy_cluster, self.marker, self.tomas_layout]
        return options

    def options(self):
        return ['Change Color', 'Processing with Scanpy', 'Clustering with Scanpy', 'Find Marker Gene', 'TOMAS']

# TOMAS
def get_attr():
    api = connection()
    to_json = api.get_attributes()
    data_dict = json.loads(to_json)
    group = data_dict['selected_group']
    cluster_list = api.get_group_dict()[group]
    return group, cluster_list

def tomas_callback1(group, show_clusters):
    layout = curdoc().get_model_by_name('tomas_layout')
    api = connection()
    adata = api.get_anndata()
    adata.obs['total_UMIs'] = np.ravel(adata.X.sum(1))
    adata.obs['log10_totUMIs'] = np.log10(adata.obs['total_UMIs'])

    figure1 = tm.vis.UMI_hist(adata,
                x_hist='log10_totUMIs',
                groupby=group,
                show_groups=show_clusters,
                return_fig=True)
    # Save it to a temporary buffer.
    buf = BytesIO()
    figure1.savefig(buf, format="png")
    # Embed the result in the html output.
    output1 = base64.b64encode(buf.getbuffer()).decode("ascii")
    div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output1))
    layout.children.append(div)
    api.set_obs(adata.obs)

def tomas_callback2(group, show_clusters):
    layout = curdoc().get_model_by_name('tomas_layout')
    api = connection()
    adata = api.get_anndata()
    tm.fit.logN_para(adata,
                 logUMIby='log10_totUMIs',
                 groupby=group,
                 groups=show_clusters,
                 inplace=True)
    r1 = 10**(adata.uns['logUMI_para'].loc[show_clusters[0],'mean']-adata.uns['logUMI_para'].loc[show_clusters[0],'mean'])
    r2 = 10**(adata.uns['logUMI_para'].loc[show_clusters[2],'mean']-adata.uns['logUMI_para'].loc[show_clusters[0],'mean'])
    string = 'With raw UMIs, total UMI ratio of<br/>'+'&nbsp;&nbsp;'+show_clusters[1]+' : '+show_clusters[0] +' = '+str(r1)+',<br>&nbsp;&nbsp;Hetero-doublet : '+show_clusters[0] +' = '+str(r2)+'<br/>'
    div = Div(text=string)
    layout.children.append(div)
    api.set_obs(adata.obs)
    api.set_uns(adata.uns)

def tomas_callback3(group, show_clusters):
    layout = curdoc().get_model_by_name('tomas_layout')
    div = Div(text='This may take a long time. Please wait...', name='Reminder')
    #div = Div(text='<img src="images/loading.gif">')
    layout.children.append(div)
    def process():       
        api = connection()
        adata = api.get_anndata()
        print(os.getcwd())
        size = os.path.getsize('./output/Tcells')
        if size == 0:
            tm.fit.dmn(adata,
                    groupby=group,
                    groups=show_clusters[0:2], 
                    c_version=True,
                    #subset=100,
                    output='./output/Tcells')
        else:
            p = pd.read_csv('./output/Tcells/alpha.csv',index_col=0)
            print(p)
            adata.varm['para_diri'] = pd.read_csv('./output/Tcells/alpha.csv',index_col=0)
        figure2 = tm.vis.dmn_convergence(show_clusters[0],output='./output/Tcells',return_fig=True)
        figure3 = tm.vis.dmn_convergence(show_clusters[1],output='./output/Tcells',return_fig=True)
        div = curdoc().get_model_by_name('Reminder')
        layout.children.remove(div)
        # Save it to a temporary buffer.
        buf = BytesIO()
        figure2.savefig(buf, format="png")
        output2 = base64.b64encode(buf.getbuffer()).decode("ascii")
        figure3.savefig(buf, format="png")
        output3 = base64.b64encode(buf.getbuffer()).decode("ascii")
        div1 = Div(text='<b>'+show_clusters[0]+'</b>')
        div2 = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output2))
        layout.children.append(column(div1, div2))
        div3 = Div(text='<b>'+show_clusters[1]+'</b>')
        div4 = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output3))
        layout.children.append(column(div3, div4))
        api.set_obs(adata.obs)
        api.set_varm(adata.varm)    
    curdoc().add_next_tick_callback(process)

def tomas_callback4(group,show_cluster):
    layout = curdoc().get_model_by_name('tomas_layout')
    div = Div(text='<b>This may take a long time. Please wait...</b>', name='Reminder')
    layout.children.append(div)
    def process():
        layout = curdoc().get_model_by_name('tomas_layout')
        api = connection()
        adata = api.get_anndata()
        tm.auxi.cal_KL_bc(adata,groups=show_cluster[0:2])
        adata_dbl_mg = tm.auxi.get_dbl_mg_bc(adata,
                                            groupby = group,
                                            groups = show_cluster,
                                            save_path = './output/Tcells') #'./prepareForRepo/re_test/test')
        try:
            r_list = np.loadtxt('./output/Tcells/Homo-naive_Homo-activated_dbl_Rest.txt')
        except:
            r_list = tm.infer.ratio_2types(adata_dbl_mg, output='./output/Tcells')#'./prepareForRepo/re_test/test')        
            np.savetxt('./output/Tcells/Homo-naive_Homo-activated_dbl_Rest.txt',r_list)
        figure5 = tm.vis.logRatio_dist(r_list, return_fig=True)
        buf = BytesIO()
        figure5.savefig(buf, format="png")
        output5 = base64.b64encode(buf.getbuffer()).decode("ascii")
        div5 = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output5))
        div1 = Div(text='<b>Estimate R with synthetic droplets</b>')
        layout.children.remove(div)
        layout.children.append(column(div1,div5))        
    curdoc().add_next_tick_callback(process)

def tomas_callback5(group, show_cluster):
    layout = curdoc().get_model_by_name('tomas_layout')
    api = connection()
    adata = api.get_anndata()
    figure6 = tm.vis.corrected_UMI_hist(adata,
                                        groupby = group,
                                        groups = show_cluster,
                                        reference = show_cluster[0],
                                        logUMIby = 'log10_totUMIs',
                                        ratios = [1,4.3,5.3],
                                        return_fig=True)
    buf = BytesIO()
    figure6.savefig(buf, format="png")
    output6 = base64.b64encode(buf.getbuffer()).decode("ascii")
    div6 = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output6))
    div1 = Div(text='<b>The total UMI distribution</b>')
    layout.children.append(div1)
    layout.children.append(div6)

### Examples to add buttons ### 
def change_color(): 
    plot_function().show_checked()
    trans = connection()
    to_json = trans.get_attributes()
    data_dict = json.loads(to_json)
    color = data_dict['selected_color']
    selected_class = data_dict['checked_class']
    group = data_dict['selected_group']
    group_dict = trans.get_group_dict()
    group_dict[group]['color'][[i for i in selected_class]] = color   
    trans.set_group_dict(group_dict)
    indices = data_dict['selected_indices']
    data_color = data_dict['data_color']
    for i in indices:
        data_color[i] = color
    # Save change of data into the Figure
    data_dict['data_color'] = data_color
    trans.set_attributes(data_dict)
    plot_function().change_checkbox_color()

def show_gene_percentage():
    layout = curdoc().get_model_by_name('scanpy_fucntions')
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
    layout = curdoc().get_model_by_name('scanpy_fucntions')
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
    layout = curdoc().get_model_by_name('scanpy_fucntions')
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
    layout = curdoc().get_model_by_name('scanpy_fucntions')
    change = connection()
    adata = change.get_anndata()

    sc.pp.highly_variable_genes(adata, min_mean=float(min_mean), max_mean=float(max_mean), min_disp=float(min_disp))
    figure = sc.pl.highly_variable_genes(adata, show=False)

    buf = BytesIO()
    figure.figure.savefig(buf, format="png")
    output1 = base64.b64encode(buf.getbuffer()).decode("ascii")
    div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(output1))
    layout.children.append(div)


def pca():
    layout = curdoc().get_model_by_name('scanpy_cluster')
    change = connection()
    adata = change.get_anndata()

    sc.tl.pca(adata, svd_solver='arpack')
    sc.pl.pca_variance_ratio(adata, log=True, save='.png')

    img = open('figures/pca_variance_ratio.png','rb')
    img_base64 = base64.b64encode(img.read()).decode("ascii")
    div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
    layout.children.append(div)
    change.set_obsm(adata.obsm)

def neighborhood_graph(neighbor_num, pc_num, resolution):
    layout = curdoc().get_model_by_name('scanpy_cluster')
    change = connection()
    adata = change.get_anndata()

    adata = sc.pp.neighbors(adata, n_neighbors=int(neighbor_num), n_pcs=int(pc_num), copy=True)
    sc.tl.umap(adata)
    sc.tl.leiden(adata, resolution=float(resolution))
    print('new')

    change.set_obsm(adata.obsm)
    change.set_uns(adata.uns)
    change.set_obs(adata.obs, set_group_name=['leiden'])

def find_marker(groupby='leiden',test_method='t-test',rank_n_genes=25):
    layout = curdoc().get_model_by_name('find_marker')
    change = connection()
    adata = change.get_anndata()

    sc.tl.rank_genes_groups(adata, groupby, method=test_method)
    sc.pl.rank_genes_groups(adata, n_genes=rank_n_genes, sharey=False, save='.png')

    img = open('figures/rank_genes_groups_leiden.png','rb')
    img_base64 = base64.b64encode(img.read()).decode("ascii")
    div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
    layout.children.append(div)
    change.set_obsm(adata.obsm)

