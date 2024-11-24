import scanpy as sc
import sys
from bokeh.palettes import d3
import base64
from pathlib import Path
from bokeh.models import Button, TextInput, Div
color_list = d3['Category20c'][20]
sys.path.append(str(Path(__file__).resolve().parents[3]))
from bokeh.layouts import row, column
from Pantheon.scpantheon.widgets import Widgets
from bokeh.io import curdoc
import data as dt
import tabs as tb


class Widgets_Color(Widgets):
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
        self.init_sccluster()
        super().init_tab()
    
    def init_sccluster(self):
        sc_cluster_step1 = Button(label='Step1: Run PCA', button_type='success')
        sc_cluster_step1.on_click(lambda : self.pca())
        cl_input1 = TextInput(title='Neighbor Num:', value='10')
        cl_input2 = TextInput(title='Principal Component Num:', value='40')
        cl_input3 = TextInput(title='Resolution', value='1')
        sc_cluster_step2 = Button(label='Step2: Clustering with Neighborhood Graph', button_type='success')
        sc_cluster_step2.on_click(lambda: self.neighborhood_graph(cl_input1.value, cl_input2.value, cl_input3.value))
        widgets_dict = {
            'sc_cluster_step1': sc_cluster_step1,
            'cl_input1': cl_input1,
            'cl_input2': cl_input2,
            'cl_input3': cl_input3,
            'sc_cluster_step2': sc_cluster_step2
        }
        merged_dict = {**self.widgets_dict, **widgets_dict}
        self.widgets_dict = merged_dict
    

    def pca(self):
        tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        def next_pca(self):
            sc.tl.pca(dt.adata, svd_solver='arpack')
            dt.init_data(dt.adata)
            # sc.pl.pca_variance_ratio(dt.adata, log=True)
            # sc.pl.pca_variance_ratio(dt.adata, log=True, save='.png')
            # img = open('figures/pca_variance_ratio.png','rb')
            # img_base64 = base64.b64encode(img.read()).decode("ascii")
            # pca_img = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
            # widgets_dict = {'pca_img': pca_img}
            # merged_dict = {**self.widgets_dict, **widgets_dict}
            # self.widgets_dict = merged_dict
            super().init_map('X_pca')
            super().init_coordinates()
            super().update_plot_source_by_coords()
            super().plot_coordinates()
            self.update_layout()
            self.view_tab()
            tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        curdoc().add_next_tick_callback(lambda: next_pca(self))

    def neighborhood_graph(self, neighbor_num, pc_num, resolution):
        tb.mute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        def next_neighborhood_graph(self, neighbor_num, pc_num, resolution):
            dt.adata.obsm['X_pca'] = dt.adata.obsm["X_pca"].to_numpy()
            sc.pp.neighbors(dt.adata, n_neighbors=int(neighbor_num), n_pcs=int(pc_num))
            sc.tl.umap(dt.adata)
            sc.tl.leiden(dt.adata, resolution=float(resolution), flavor="igraph", n_iterations=2, directed=False)
            dt.init_data(dt.adata)
            super().init_map('X_umap')
            super().init_coordinates()
            super().create_group_select('leiden')
            super().update_plot_source_by_coords()
            super().plot_coordinates()
            self.update_layout()
            self.view_tab()
            tb.unmute_global(tb.panel_dict, tb.curpanel, tb.ext_widgets)
        curdoc().add_next_tick_callback(lambda: next_neighborhood_graph(self, neighbor_num, pc_num, resolution))


    def update_layout(self):
        super().update_layout()
        sccluster_key = ['sc_cluster_step1', 'cl_input1', 'cl_input2', 'cl_input3', 'sc_cluster_step2']
        values = [self.widgets_dict[key] for key in sccluster_key if key in self.widgets_dict]
        layout_sccluster = column(values)

        pca_img_key = ['pca_img']
        values = [self.widgets_dict[key] for key in pca_img_key if key in self.widgets_dict]
        layout_pca_img = column(values)
        self.layout = column([self.layout, row([layout_sccluster, layout_pca_img])])
