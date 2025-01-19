# # -*- coding: utf-8 -*-
import scanpy as sc
import sys
from bokeh.palettes import d3
import base64
from pathlib import Path
color_list = d3['Category20c'][20]
sys.path.append(str(Path(__file__).resolve().parents[3]))
from bokeh.layouts import row, column
from scpantheon.widgets import Widgets
from scpantheon.buttons import Widget_type, make_widget
from bokeh.io import curdoc
import tabs as tb
import data as dt


class Widgets_Ext(Widgets):
    def __init__(self,
        name: str | None = 'generic columns',
    ):
        """
        dt.adata: handle with anndata structure  
        .obs: a pd.Dataframe with cell names as index, color and group name as columns  
        denotes a certain cell's current visualized color and which cluster it belongs to in each group  
        .uns: a dict {map_name: {group_name : pd.Dataframe}}  
        pd.Dataframe's index are cluster names, columns are color and cell_num  
        denotes each cluster's color and cell number
        """
        super().__init__(name)
        self.init_extension()
        super().init_tab()
    
    def init_extension(self):

        """customize widgets and callback for this extension"""
        sc_cluster_step1_arg = {'label': 'Step1: Run PCA', 'button_type': 'success'}
        sc_cluster_step1 = make_widget(Widget_type.button, lambda : self.pca(), **sc_cluster_step1_arg)
        print(sc_cluster_step1)
        cl_input1_arg = {'title': 'Neighbor Num:', 'value': '10'}
        cl_input1 = make_widget(Widget_type.text, **cl_input1_arg)
        cl_input2_arg = {'title':'Principal Component Num:', 'value': '40'}
        cl_input2 = make_widget(Widget_type.text, **cl_input2_arg)
        cl_input3_arg = {'title':'Resolution:', 'value': '1'}
        cl_input3 = make_widget(Widget_type.text, **cl_input3_arg)
        sc_cluster_step2_arg = {'label': 'Step2: Clustering with Neighborhood Graph', 'button_type': 'success'}
        sc_cluster_step2 = make_widget(
            Widget_type.button,
            lambda: self.neighborhood_graph(cl_input1.value, cl_input2.value, cl_input3.value),
            **sc_cluster_step2_arg
            )
        
        """
        Add customized widgets to widgets_dict. 
        Only widgets in widgets_dict need to be modified.
        """
        widgets_dict = {          
            'sc_cluster_step1': sc_cluster_step1,
            'cl_input1': cl_input1,
            'cl_input2': cl_input2,
            'cl_input3': cl_input3,
            'sc_cluster_step2': sc_cluster_step2
        }
        self.widgets_dict = {**self.widgets_dict, **widgets_dict}

    def pca(self):
        tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        def next_pca(self):
            """
            Define callback function for customized widgets here. 
            If more parameters are needed, 
            add them in "def pca(self)" (line 65) and "def next_pca(self)" (line 67)
            """
            """
            Use scPantheon global data instance "dt.adata" for functions require anndata inputs.
            """
            sc.tl.pca(dt.adata, svd_solver='arpack')
            """
            If a new map(coordinate system) is generated in anndata.obsm, 
            call dt.init_data with the key of the generated obsm.
            It formats the obsm into pd.Dataframe, which supports clustering operations in scPantheon.
            """
            dt.init_data(dt.adata, 'X_pca')

            """
            If you want to display other widgets, it's also feasible to define customed widgets here
            """
            sc.pl.pca_variance_ratio(dt.adata, log=True)
            sc.pl.pca_variance_ratio(dt.adata, log=True, save='.png')
            img = open('figures/pca_variance_ratio.png','rb')
            img_base64 = base64.b64encode(img.read()).decode("ascii")
            pca_img = make_widget(Widget_type.div, text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
            widgets_dict = {'pca_img': pca_img}
            self.widgets_dict = {**self.widgets_dict, **widgets_dict}
            """
            Update visualization and format dt.adata back to the way scPantheon supports. 
            If only a certain obsm is modified, update with parameter new_obsm and corresponding obsm name
            If multiple obsm is modified, update with new_obsm = None. It updates the whole anndata by default.
            If a new coordinate system is generated, update with parameter new_map and corresponding obsm name
            If a new group is generated, update with parameter new_group and corresponding obs name
            """
            super().update_tab(new_obsm = 'X_pca', new_map = 'X_pca' )
            tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        curdoc().add_next_tick_callback(lambda: next_pca(self))

    def neighborhood_graph(self, neighbor_num, pc_num, resolution):
        tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        def next_neighborhood_graph(self, neighbor_num, pc_num, resolution):
            
            """
            The type of dt.adata.obsm is pd.Dataframe by default. 
            Format dt.adata.obsm if necessary in following operations
            """
            dt.adata.obsm['X_pca'] = dt.adata.obsm['X_pca'].to_numpy()

            """main operations in callback function"""
            sc.pp.neighbors(dt.adata, n_neighbors=int(neighbor_num), n_pcs=int(pc_num))
            sc.tl.umap(dt.adata)
            sc.tl.leiden(dt.adata, resolution=float(resolution), flavor="igraph", n_iterations=2, directed=False)

            """
            Update visualization and format dt.adata back to the way scPantheon supports. 
            If only a certain obsm is modified, update with parameter new_obsm and corresponding obsm name
            If multiple obsm is modified, update with new_obsm = None. It updates the whole anndata by default.
            If a new coordinate system is generated, update with parameter new_map and corresponding obsm name
            If a new group is generated, update with parameter new_group and corresponding obs name
            """
            super().update_tab(new_obsm = 'X_umap', new_map = 'X_umap', new_group = 'leiden')

            tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        curdoc().add_next_tick_callback(lambda: next_neighborhood_graph(self, neighbor_num, pc_num, resolution))


    def update_layout(self):
        super().update_layout()

        """
        Arrange layout.
        You only need to change widget names in sccluster_key below according to keys in "widgets_dict" (line 56),
        column(list) arrange widgets or layouts in a column. row(list) arrange widgets or layouts in a row.
        """
        sccluster_key = ['sc_cluster_step1', 'cl_input1', 'cl_input2', 'cl_input3', 'sc_cluster_step2']
        values = [self.widgets_dict[key] for key in sccluster_key if key in self.widgets_dict]
        layout_sccluster = column(values)

        pca_img_key = ['pca_img']
        values = [self.widgets_dict[key] for key in pca_img_key if key in self.widgets_dict]
        layout_pca_img = column(values)

        """Merge it with basic layout with format self.layout = column([self.layout, _____ ])"""
        self.layout = column([self.layout, row([layout_sccluster, layout_pca_img])])