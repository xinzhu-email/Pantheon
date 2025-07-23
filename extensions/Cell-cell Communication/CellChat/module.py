from scpantheon.buttons import make_layout, make_widget, Widget_type, LayoutOrientation
from scpantheon.widgets.extensionAPI import Prerequisite, ResultSelector
from scpantheon.stdata import DataCat
from scpantheon.tabs import refresh
from anndata import AnnData

def prefix_str2list(prefix_str: str):
    return list(dict.fromkeys([prefix.strip() for prefix in prefix_str.split(',')]))

def prefix_list2str(prefix_list: list):
    return ", ".join(list(dict.fromkeys(prefix_list)))

class PanelExt():
    def __init__(self, func_name, ext_name):
        # Don't change anything in __init__ function except those lines labelled with TODO
        self.func_name = func_name
        self.ext_name = ext_name
        self.widgets_dict = dict()
        self.layouts_dict = dict()
        self.prefix = dict()
        self.data = AnnData()

        # TODO: change the list of tuple of the input data required by your method and the corresponding prompt
        self.prereq = Prerequisite(self.ext_name, [(DataCat.EXPMATRIX, "Select Expression Matrix")]) 

        # TODO: change the list of tuple of the input data output of your method and the corresponding prompt
        self.res = ResultSelector(self.ext_name, [(DataCat.Data_var, "Gene Value Variables"), (DataCat.Data_obs, "Cell Value Variables")])
        
        self.init_widget_dict()
        self.layout = self.init_layout()
    
    def init_widget_dict(self):
        # TODO: make your own widgets
        self.ext_title = make_widget(
            Widget_type.div,
            text = f"<div style='font-size: 40px;'>{self.ext_name}"
        )
        prefix_title = make_widget(
            Widget_type.div,
            text = "Define Prefix for Mitochondrial, Ribosomal, Hemoglobin Genes, etc."
        )
        prefix_label = make_widget(
            Widget_type.text,
            lambda: self.prefix_label_callback(),
            value = "mt",
            title = "Define Prefix Label (to be Showed in Plots)"
        )
        prefix_value = make_widget(
            Widget_type.text,
            lambda: self.prefix_value_callback(),
            value = "MT-",
            title = "Define Corresponding Prefix"
        )
        prefix_exec = make_widget(
            Widget_type.button,
            lambda: self.prefix_exec_callback(),
            label = "Define Gene by Prefix"
        )
        prefix_dtitle = make_widget(Widget_type.div, text = "Prefix Defined")
        prefix_dspl = make_widget(
            Widget_type.checkBoxGroup,
            labels = [],
            active = []
        )
        prefix_cancel = make_widget(
            Widget_type.button,
            lambda: self.prefix_cancel_callback,
            label = "Delete Selected Prefix Definition"
        )
        qc_mode = make_widget(
            Widget_type.checkBoxGroup,
            labels = ['Calculate QC_metrics in log1p Mode'],
            active = [0]
        )
        prefix_qc = make_widget(
            Widget_type.button,
            lambda: self.prefix_qc_callback(),
            label = "Calculate QC_metrics with Selected Prefix"
        )
        self.widgets_dict = {
            'prereq': self.prereq,
            'prefix_title': prefix_title,
            'prefix_label': prefix_label,
            'prefix_value': prefix_value,
            'prefix_exec': prefix_exec,
            'prefix_dtitle': prefix_dtitle,
            'prefix_dspl': prefix_dspl,
            'prefix_cancel': prefix_cancel,
            'qc_mode': qc_mode,
            'prefix_qc': prefix_qc,
            'res': self.res
        }

    def init_layout(self):
        # TODO: make your layout
        layout_align = make_layout(self.widgets_dict, ['prefix_label', 'prefix_value'], LayoutOrientation.horizontal)
        self.layouts_dict = {
            'prefix_title': self.widgets_dict['prefix_title'],
            'prefix_exec': self.widgets_dict['prefix_exec'],
            'prefix_dtitle': self.widgets_dict['prefix_dtitle'],
            'prefix_dspl': self.widgets_dict['prefix_dspl'],
            'prefix_qc': self.widgets_dict['prefix_qc'],
            'prefix_cancel': self.widgets_dict['prefix_cancel'],
            'qc_mode': self.widgets_dict['qc_mode'],
            'prefix_align': layout_align,
        }
        self.layouts_dict['prefix_define'] = make_layout(self.layouts_dict, ['prefix_align', 'prefix_exec'])
        return make_layout(self.layouts_dict, ['prefix_title', 'prefix_define', 'prefix_dtitle', 'prefix_dspl', 'prefix_cancel', 'qc_mode', 'prefix_qc'])

    def prefix_exec_callback(self):
        if self.widgets_dict['prefix_label'].value not in list(self.prefix.keys()):
            self.prefix[self.widgets_dict['prefix_label'].value] = prefix_str2list(self.widgets_dict['prefix_value'].value)
        else:
            self.prefix[self.widgets_dict['prefix_label'].value] += prefix_str2list(self.widgets_dict['prefix_value'].value)
        labels = []
        active = []
        active_prefix_labels = [self.widgets_dict['prefix_dspl'].labels[i].split(":")[0] for i in self.widgets_dict['prefix_dspl'].active]
        prefix_keys = list(self.prefix.keys())
        for i in range(len(prefix_keys)):
            key = prefix_keys[i]
            labels.append(key + ": with prefix " + prefix_list2str(self.prefix[key]))
            if key in active_prefix_labels:
                active.append(i)
        refresh_id = self.widgets_dict['prefix_dspl'].id
        self.widgets_dict['prefix_dspl'] = make_widget(
            Widget_type.checkBoxGroup,
            None,
            labels = labels,
            active = active
        )
        refresh(refresh_id, self.widgets_dict['prefix_dspl'])

    def prefix_label_callback(self):
        match self.widgets_dict['prefix_label'].value:
            case "mt":
                self.widgets_dict['prefix_value'].value = "MT-"
            case "ribo":
                self.widgets_dict['prefix_value'].value = "RPS, RPL"
            case "hb":
                self.widgets_dict['prefix_value'].value = "^HB[^(P)]"
        # TODO: refresh
    
    def prefix_value_callback(self):
        prefix_list = prefix_str2list(self.widgets_dict['prefix_value'].value)
        prefix_string = prefix_list2str(prefix_list)
        if prefix_string != self.widgets_dict['prefix_value'].value:
            self.widgets_dict['prefix_value'].value = prefix_string
        # match prefix_list:
        #     case ["MT-"]:
        #         self.widgets_dict['prefix_label'].value = "mt"
        #     case ["RPS"]:
        #         self.widgets_dict['prefix_label'].value = "ribo"
        #     case ["RPL"]:
        #         self.widgets_dict['prefix_label'].value = "ribo"
        #     case ["RPL", "RPS"]:
        #         self.widgets_dict['prefix_label'].value = "ribo"
        #     case ["^HB[^(P)]"]:
        #         self.widgets_dict['prefix_label'].value = "hb"
        # tb.view_panel(tb.panel_dict, tb.ext_layout, tb.ext_widgets, tb.curpanel)

    def prefix_qc_callback(self):
        pass
        # active_prefix_labels = [self.widgets_dict['prefix_dspl'].labels[i].split(":")[0] for i in self.widgets_dict['prefix_dspl'].active]
        # for prefix_label in active_prefix_labels:
        #     prefix_tuple = tuple(self.prefix[prefix_label])
        #     dt.adata.var[prefix_label] = dt.adata.var_names.str.startswith(prefix_tuple)
        # # self.dtprocessor.insert_cluster(dt.adata, PlotBase.gene, from_data = True, column_names = active_prefix_labels)
        # sc.pp.calculate_qc_metrics(
        #     dt.adata, qc_vars = active_prefix_labels, inplace=True, log1p=False
        # )
        # var_list = ['n_cells_by_counts', 'mean_counts', 'pct_dropout_by_counts', 'total_counts']
        # obs_list = ['n_genes_by_counts', 'total_counts', 'pct_counts_in_top_50_genes', 'pct_counts_in_top_100_genes', 'pct_counts_in_top_200_genes', 'pct_counts_in_top_500_genes']
        # for label in active_prefix_labels:
        #     obs_list = obs_list + ["total_counts_" + label, "pct_counts_" + label]
        # # self.dtprocessor.insert_data(dt.adata, PlotBase.gene, from_data = True, column_names = var_list)
        # # self.dtprocessor.insert_data(dt.adata, PlotBase.cell, from_data = True, column_names = obs_list)
        # # print(dt.adata.varm['scpantheon'])
        # # print(dt.adata.obsm['scpantheon'])
        # tb.view_panel(tb.panel_dict, tb.ext_layout, tb.ext_widgets, tb.curpanel)                
    
    def prefix_cancel_callback(self):
        pass