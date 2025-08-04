from enum import Enum 
from functools import reduce
from anndata import AnnData
from bokeh.plotting import figure 
from bokeh.models import ColumnDataSource, HoverTool, Arrow, OpenHead, LinearAxis
from scpantheon.front_end.data_qt import dir, read_path
import pandas as pd
import numpy as np
import scanpy as sc
import networkx as nx
import os
# import logging
# logger = logging.getLogger(__name__)


def fast_reduce_intersection(*lists):
    if not lists:
        return []    
    first = lists[0]
    common = reduce(lambda a, b: a & set(b), lists[1:], set(first))
    return [x for x in first if x in common]


class ValidCache:
    def __init__(self, adata: AnnData):
        self.valid_var = list(range(adata.n_vars))
        self.valid_obs = list(range(adata.n_obs))
    
    def update_valid_var(self, varlist: list):
        self.valid_var = varlist
    
    def update_valid_obs(self, obslist: list):
        self.valid_obs = obslist


class Streamline(Enum):
    RAW = 'Raw'
    QUALITY_CONTROL = 'Quality Control'
    NORM = 'Normalization'
    GENE_ANALYSIS = 'Gene Analysis'
    IMPUTATION = 'Data Imputation'
    DIMENSIONALITY_REDUCTION = 'Dimensionality Reduction'
    CLUSTERING = 'Clustering'
    TRAJECTORY = 'Trajectory'
    DE = 'Differential Expression'
    GRN = 'Gene Regulatory Network'
    CELL_COMMUNICATION = 'Cell-Cell Communication'
    CUSTOMIZED = 'Customized'


class DataCat(Enum):
    EXPMATRIX = "exp_matrix"
    HDCoordinate = "hd_coordinate" # TODO: a better name for layers
    LDCoordinate_var = "var_embedding"
    LDCoordinate_obs = "obs_embedding"
    Catagorial_var = "var_categorical"
    Catagorial_obs = "obs_categorical"
    Data_var = "var_data"
    Data_obs = "obs_data"
    Pairwise_var = "var_pairwise"
    Pairwise_obs = "obs_pairwise"
    Unstructured = "uns"

class ExtAdataManager:
    def __init__(
        self, 
        streamline: Streamline = Streamline.RAW,
        ext_name: str = "None",
        exp_matrix: list[str] = ["X"],
        var_valid: list[int] | list[str] | None = [],
        obs_valid: list[int] | list[str] | None = [],
        var_categorical: list[str] | None = [],
        obs_categorical: list[str] | None = [],
        var_data: list[str] | None = [],
        obs_data: list[str] | None = [],
        var_embedding: list[str] | None = [],
        obs_embedding: list[str] | None = [],
        var_pairwise: list[str] | None = [],
        obs_pairwise: list[str] | None = [],
        hd_coordinate: list[str] | None = [],
        unstructured: list[str] | None = []
    ):
        """exp_matrix: send out by default"""
        self.var_valid = var_valid #11
        self.obs_valid = obs_valid
        self.kwargs = {"streamline": streamline, "ext_name": ext_name}
        self.kwargs["exp_matrix"] = ["X"]
        self.kwargs["var_categorical"] = var_categorical
        self.kwargs["obs_categorical"] = obs_categorical
        self.kwargs["var_data"] = var_data
        self.kwargs["obs_data"] = obs_data
        self.kwargs["var_embedding"] = var_embedding
        self.kwargs["obs_embedding"] = obs_embedding
        self.kwargs["var_pairwise"] = var_pairwise
        self.kwargs["obs_pairwise"] = obs_pairwise
        self.kwargs["hd_coordinate"] = hd_coordinate
        self.kwargs["unstructured"] = unstructured
    
    def make_ext_data(
        self, 
        adata: AnnData,
    ):
        """exp_matrix: send out by default"""
        
        ext_adata = AnnData(
            X=adata.X.copy()
        )
        var_lists_to_intersect = [adata.var_names]
        if self.var_valid:
            if all(isinstance(x, int) for x in self.var_valid):
                ext_var_valid = [adata.var_names[i] for i in self.var_valid]
                var_lists_to_intersect.append(ext_var_valid)
            elif all(isinstance(x, str) for x in self.var_valid):
                ext_var_valid = self.var_valid
            # TODO: warning for wrong type
        if self.kwargs["var_categorical"]:
            categorical_var_names = adata.var_names[~adata.var[self.kwargs["var_categorical"]].isna().any(axis=1)].tolist()
            var_lists_to_intersect.append(categorical_var_names)
            ext_adata.var = adata.var[self.kwargs["var_categorical"]]
        if self.kwargs["var_data"]:
            data_var_names = adata.var_names[~adata.var[self.kwargs["var_data"]].isna().any(axis=1)].tolist()
            var_lists_to_intersect.append(data_var_names)
            ext_adata.var = pd.concat([ext_adata.var, adata.var[self.kwargs["var_data"]]], axis = 1)
        if self.kwargs["var_embedding"]:
            for key in self.kwargs["var_embedding"]:
                ext_adata.varm[key] = adata.varm[key]
            mask = np.all([~np.isnan(adata.varm[key]).any(axis = 1) for key in self.kwargs["var_embedding"]], axis=0)
            varm_var_names = adata.var_names[mask].tolist()
            var_lists_to_intersect.append(varm_var_names)
        if self.kwargs["var_pairwise"]:
            for key in self.kwargs["var_pairwise"]:
                ext_adata.varp[key] = adata.varp[key]
            mask = np.all([~np.isnan(adata.varp[key]).any(axis = 1) for key in self.kwargs["var_pairwise"]], axis=0)
            varp_var_names = adata.var_names[mask].tolist()
            var_lists_to_intersect.append(varp_var_names)
        if self.kwargs["hd_coordinate"]:
            # TODO: repeated names
            for key in self.kwargs["hd_coordinate"]:
                ext_adata.layers[key] = adata.layers[key]
            mask = np.all([~np.isnan(adata.layers[key]).any(axis = 0) for key in self.kwargs["hd_coordinate"]], axis=0)
            layers_var_names = adata.var_names[mask].tolist()
            var_lists_to_intersect.append(layers_var_names)
        if len(var_lists_to_intersect) == 1:
            ext_adata_var_names = adata.var_names
        else:
            ext_adata_var_names = fast_reduce_intersection(*var_lists_to_intersect)
        
        obs_lists_to_intersect = [adata.obs_names]
        if self.obs_valid:
            if all(isinstance(x, int) for x in self.obs_valid):
                ext_obs_valid = [adata.obs_names[i] for i in self.obs_valid]
                obs_lists_to_intersect.append(ext_obs_valid)
            elif all(isinstance(x, str) for x in self.obs_valid):
                ext_obs_valid = self.obs_valid
            # TODO: warning for wrong type
        if self.kwargs["obs_categorical"]:
            categorical_obs_names = adata.obs_names[~adata.obs[self.kwargs["obs_categorical"]].isna().any(axis=1)].tolist()
            obs_lists_to_intersect.append(categorical_obs_names)
            ext_adata.obs = adata.obs[self.kwargs["obs_categorical"]]
        if self.kwargs["obs_data"]:
            data_obs_names = adata.obs_names[~adata.obs[self.kwargs["obs_data"]].isna().any(axis=1)].tolist()
            obs_lists_to_intersect.append(data_obs_names)
            ext_adata.obs = pd.concat([ext_adata.obs, adata.obs[self.kwargs["obs_data"]]], axis = 1)
        if self.kwargs["obs_embedding"]:
            for key in self.kwargs["obs_embedding"]:
                ext_adata.obsm[key] = adata.obsm[key]
            mask = np.all([~np.isnan(adata.obsm[key]).any(axis = 1) for key in self.kwargs["obs_embedding"]], axis=0)
            obsm_obs_names = adata.obs_names[mask].tolist()
            obs_lists_to_intersect.append(obsm_obs_names)
        if self.kwargs["obs_pairwise"]:
            for key in self.kwargs["obs_pairwise"]:
                ext_adata.obsp[key] = adata.obsp[key]
            mask = np.all([~np.isnan(adata.obsp[key]).any(axis = 1) for key in self.kwargs["obs_pairwise"]], axis=0)
            obsp_obs_names = adata.obs_names[mask].tolist()
            obs_lists_to_intersect.append(obsp_obs_names)
        if self.kwargs["hd_coordinate"]:
            mask = np.all([~np.isnan(adata.layers[key]).any(axis = 1) for key in (self.kwargs["hd_coordinate"] - ["X"])], axis=0)
            layers_obs_names = adata.obs_names[mask].tolist()
            obs_lists_to_intersect.append(layers_obs_names)
        if self.kwargs["unstructured"]:
            for key in self.kwargs["unstructured"]:
                ext_adata.uns[key] = adata.uns[key]
        if len(obs_lists_to_intersect) == 1:
            ext_adata_obs_names = adata.obs_names
        else:
            ext_adata_obs_names = fast_reduce_intersection(*obs_lists_to_intersect)
        ext_adata.var_names = adata.var_names
        ext_adata.obs_names = adata.obs_names
        subdata = ext_adata[ext_adata_obs_names, ext_adata_var_names]
        return subdata

        # TODO: problem: useful NaN


class ExtInfo:
    def __init__(self, name: str, streamline: str):
        self.name = name
        self.streamline = streamline
        self.valid_gene = list[int]()
        self.valid_cell = list[int]()
        self.parents = dict()
        self.results = dict()
    
    def update_valid(self, var_valid: list[int] | None = None, obs_valid: list[int] | None = None):
        if obs_valid is not None:
            self.valid_cell = obs_valid
        if var_valid is not None:
            self.valid_gene = var_valid
    
class DiGplot:
    def __init__(self):
        self.G = nx.DiGraph()
        self.plot = figure()
    
    def add_node(self, gene_node: ExtInfo):
        self.G.add_node(gene_node)
    
    def update_node_by_node(self, gene_node: ExtInfo):
        for node in self.G.nodes:
            if node.name == gene_node.name:
                node = gene_node
                return
        
    def update_node_by_dataframe(self, 
        name: str, 
        data: pd.DataFrame, 
        parents: bool | None = False, 
        parentlist: list[str] | None = None,
        results: bool | None = False,
        resultlist: list[str] | None = None
    ):
        for node in self.G.nodes:
            if node.name == name:
                if parents is True:
                    if parentlist is None:
                        print("Warning: parents is to be updated but no parentlist provided")
                        break
                    else:
                        parent_dict = dict()
                        parent_node_namelist = []
                        for parent in parentlist:
                            info_line = data[data["result"] == parent]
                            if len(info_line.index) > 1:
                                print("Error: result name repeated")
                                return
                            elif len(info_line.index == 1):
                                info = f"{parent} from session: {info_line.loc[0, 'streamline']}"
                                info_key = info_line.loc[0, "type"].value
                                parent_node_namelist.append(info_line.loc[0, 'session'])
                                if info_key in parent_dict:
                                    parent_dict[info_key].append(info)
                                else: 
                                    parent_dict[info_key] = [info]
                        node.parents = parent_dict
                        parent_nodes = []
                        for node in self.G.nodes:
                            if node.name in parent_node_namelist:
                                parent_nodes.append(node)
                        self.add_edge(parent_nodes, node)
                        break
                if results is True:
                    if resultlist is None:
                        print("Warning: parents is to be updated but no parentlist provided")
                        return
                    else:
                        result_dict = dict()
                        for result in resultlist:
                            info_line = data[data["result"] == result]
                            if len(info_line.index) > 1:
                                print("Error: result name repeated")
                                return
                            info_key = info_line.loc[0, "type"].value
                            if info_key in result_dict:
                                result_dict[info_key].append(result)
                            else:
                                result_dict[info_key] = [result]
                        node.results = result_dict
                        break                    
    
    def update_node_valid(self, name: str, var_valid: list[int] | None = None, obs_valid: list[int] | None = None):
        for node in self.G.nodes:
            if node.name == name:
                node.update_valid(var_valid, obs_valid)
                return
    
    def add_edge(self, node_start_list, node_end):
        for node_start in node_start_list:
            self.G.add_edge(node_start, node_end)
    
    def make_plot(self):
        pos = dict()
        streamline_list_dict = {}
        for node in self.G.nodes:
            if node.streamline in list(streamline_list_dict.keys()):
                streamline_list_dict[node.streamline].append(node)
            else:
                streamline_list_dict[node.streamline] = [node]
        n_streamline = len(list(streamline_list_dict.keys()))
        for j in range(n_streamline):
            key = list(streamline_list_dict.keys())[j]
            n_session = len(streamline_list_dict[key])
            offset = 0.1*(-1)**j
            for i in range(n_session):
                pos[streamline_list_dict[key][i]] = (2 * j, i - (n_session - 1) / 2 + offset)
        node_x = [pos[node][0] for node in self.G.nodes]
        node_y = [pos[node][1] for node in self.G.nodes]
        node_ids = [node.name for node in self.G.nodes]
        node_valid_gene = [len(node.valid_gene) for node in self.G.nodes]
        node_valid_cell = [len(node.valid_cell) for node in self.G.nodes]
        node_streamlines = [node.streamline for node in self.G.nodes]
        node_parents = [str(node.parents) for node in self.G.nodes]
        node_results = [str(node.results) for node in self.G.nodes]
        
        source = ColumnDataSource(data=dict(
            x = node_x,
            y = node_y,
            name = node_ids,
            valid_genes = node_valid_gene,
            valid_cells = node_valid_cell,
            streamline = node_streamlines,
            parents = node_parents,
            result = node_results
        ))

        scatter_size = 20
        p = figure(
            width=500,
            height=500,
            x_range=(-0.5, 15.5),
            y_range=(-2.5, 2.5),
            tools = "pan, wheel_zoom",
            active_drag = "pan",
            active_scroll = "wheel_zoom"
        )
        if not p.xaxis:
            p.xaxis = LinearAxis()
        if not p.yaxis:
            p.yaxis = LinearAxis()
        x_range = p.x_range.end - p.x_range.start
        y_range = p.y_range.end - p.y_range.start
        width_px = p.width
        height_px = p.height
        x_scale = x_range / width_px
        y_scale = y_range / height_px
        for edge in self.G.edges:
            start_pos = pos[edge[0]]
            end_pos = pos[edge[1]]
            start_pos_screen = ((start_pos[0] - p.x_range.start)/x_scale, (start_pos[1] - p.y_range.start)/y_scale)
            end_pos_screen = ((end_pos[0] - p.x_range.start)/x_scale, (end_pos[1] - p.y_range.start)/y_scale)
            mid_pos_x = (start_pos_screen[0] + end_pos_screen[0]) / 2
            mid_pos_y = (start_pos_screen[1] + end_pos_screen[1]) / 2
            dx = end_pos_screen[0] - start_pos_screen[0]
            dy = end_pos_screen[1] - start_pos_screen[1]
            length = np.sqrt(dx**2 + dy**2)
            dx = dx * (length - scatter_size) / length
            dy = dy * (length - scatter_size) / length
            start_pos_screen = (mid_pos_x - dx/2, mid_pos_y - dy/2)
            end_pos_screen = (mid_pos_x + dx/2, mid_pos_y + dy/2)
            p.add_layout(Arrow(
                end=OpenHead(line_color="black", line_width=1.5, size=8),
                x_start = start_pos_screen[0] * x_scale + p.x_range.start, y_start = start_pos_screen[1] * y_scale + p.y_range.start,
                x_end = end_pos_screen[0] * x_scale + p.x_range.start, y_end = end_pos_screen[1] * y_scale + p.y_range.start,
                line_color="black", line_alpha=1
            ))
        nodes = p.scatter(
            x = 'x', y = 'y', size=scatter_size, source = source,
            fill_color="blue", line_color="black", fill_alpha=0.8
        )
        hover = HoverTool(
            tooltips=[
                ("Name", "@name"),
                ("Valid Gene Number", "@valid_genes"),
                ("Valid Cell Number", "@valid_cells"),
                ("Streamline", "@streamline"),
                ("Parents", "@parents"),
                ("Results", "@result")
            ],
            renderers=[nodes]
        )
        p.add_tools(hover)
        p.axis.visible = False
        p.grid.visible = False
        p.toolbar.logo = None
        self.plot = p   


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

def init_data():
    adata = load_path()
    adata.uns["scpantheon"] = dict()
    adata.uns["scpantheon"]["root"] = ExtAdataManager(
        var_valid = list(range(adata.n_vars)), 
        obs_valid = list(range(adata.n_obs))
        )
    adata.uns["scpantheon_categorizor"] = {
        DataCat.Catagorial_obs.value: list[str](), 
        DataCat.Data_obs.value: list[str](),
        DataCat.Catagorial_var.value: list[str](),
        DataCat.Data_var.value: list[str]()
    }
    return adata

def extract_streamline(): 
    # TODO: examine: dir/extensions/streamline/method_name/module.py
    extensions_path = os.path.join(dir, 'extensions')
    if not os.path.exists(extensions_path):
        os.mkdir(extensions_path)
        return dict()
    
    result_dict = dict()
    for subfolder1 in os.listdir(extensions_path):
        subfolder1_path = os.path.join(extensions_path, subfolder1)
        if os.path.isdir(subfolder1_path):
            valid_subfolders = dict()
            for subfolder2 in os.listdir(subfolder1_path):
                subfolder2_path = os.path.join(subfolder1_path, subfolder2)
                if os.path.isdir(subfolder2_path):
                    module_path = os.path.join(subfolder2_path, 'module.py')
                    if os.path.exists(module_path):
                        valid_subfolders[subfolder2] = dict()
            if len(list(valid_subfolders.keys())) > 0:
                result_dict[subfolder1] = valid_subfolders
    return result_dict if result_dict else {}

def sort_streamline_list():
    fixed_streamline = [
        "Quality Control",
        "Normalization",
        "Gene Analysis", 
        "Data Imputation", 
        "Dimensionality Reduction",
        "Clustering",
        "Trajectory",
        "Differential Expression",
        "Gene Regulatory Network",
        "Cell-cell Communication"
        ]
    streamline_list = list(session_dict.keys())
    fixed = list()
    customized = list()
    for streamline in streamline_list:
        if streamline in fixed_streamline:
            fixed.append(streamline)
        else:
            customized.append(streamline)
    fixed_sorted = sorted(fixed, key=lambda x: fixed_streamline.index(x))
    return (fixed_sorted + customized)



adata: AnnData
session_dict = dict()
session_info = pd.DataFrame(data=[["raw", "X", DataCat.EXPMATRIX, "raw"]], columns = ["session", "result", "type", "streamline"])
digplot = DiGplot()
validcache: ValidCache