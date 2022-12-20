import os
import numpy as np
import pandas as pd
import scanpy as sc
from io import BytesIO
from bokeh.palettes import d3
import json
import base64
import sys
from pathlib import Path
from bokeh.io import curdoc
import tomas as tm
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
        # except:
        #     print('No Group!')

        # try:
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
            # self.tomas_layout.name = 'TOMAS'
        except:
            self.tomas_layout = column()

    def add(self):
        return self.tomas_layout

def get_attr():
    api = connection()
    to_json = api.get_attributes()
    data_dict = json.loads(to_json)
    group = data_dict['selected_group']
    cluster_list = api.get_group_dict()[group]
    return group, cluster_list

def tomas_callback1(group, show_clusters):
    layout = curdoc().get_model_by_name('TOMAS')
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
    layout = curdoc().get_model_by_name('TOMAS')
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
    layout = curdoc().get_model_by_name('TOMAS')
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
    layout = curdoc().get_model_by_name('TOMAS')
    div = Div(text='<b>This may take a long time. Please wait...</b>', name='Reminder')
    layout.children.append(div)
    def process():
        layout = curdoc().get_model_by_name('TOMAS')
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
    layout = curdoc().get_model_by_name('TOMAS')
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