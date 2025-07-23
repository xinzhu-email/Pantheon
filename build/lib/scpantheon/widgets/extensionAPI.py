from enum import Enum
from scpantheon.buttons import Widget_type, LayoutOrientation, make_widget, make_layout
from anndata import AnnData
from scpantheon.stdata import DataCat
from scpantheon.tabs import refresh
import stdata as dt


class Prerequisite:
    def __init__(
        self,
        ext_name: str,
        data_req_with_prompts: list[tuple[DataCat, str|None]]
    ):
        self.ext_name = ext_name
        self.data_type = data_req_with_prompts
        self.n_req = len(self.data_type)
        self.layout_dict = dict()
        self.widgets_dict = dict()
        self.ext_data = AnnData()
        self.init_widget_dict()
        self.layout = self.init_layout()
    
    def init_widget_dict(self):
        self.widgets_dict["prereq_title"] = make_widget(Widget_type.div, text = f"<div style='font-size: 30px;'> Data Selection")
        self.make_prereq_selections()

    def init_layout(self):
        prereq_key = ['prereq_title'] + [f"prereq_{i}" for i in range(self.n_req)]
        return make_layout(self.widgets_dict, prereq_key)
    
    def make_prereq_selections(self):
        for i in range(self.n_req):
            self.widgets_dict[f"prereq_title_{i}"] = make_widget(Widget_type.div, text = f"<div style='font-size: 20px;'> {self.data_type[i][1]}")
            resultlist = self.find_result(i)
            self.widgets_dict[f"select_result_{i}"] = make_widget(
                Widget_type.select,
                lambda: self.prereq_selection_callback(),
                options = resultlist,
                value = resultlist[0],
            )
            self.widgets_dict[f"prereq_{i}"] = make_layout(
                self.widgets_dict, 
                [f"prereq_title_{i}", f"select_result_{i}"],
                LayoutOrientation.vertical
            )

    def prereq_selection_callback(self):
        # TODO: Show choice on plot | Do nothing
        pass


    def find_result(
        self,
        i: int
    ):
        match self.data_type[i][0]:
            case DataCat.EXPMATRIX:
                resultlist = ["X"]
            case DataCat.HDCoordinate:
                resultlist = dt.adata.layers.keys()
            case _:
                resultlist = [f"{self.data_type[i][0].value}_0", f"{self.data_type[i][0].value}_1"] 
        # resultlist = [f"{self.data_type[i][1]}_{j}" for j in range(5)]
        # TODO: find list of label names/ column names of self.data_type[i][0] in stdata.adata
        return resultlist

class ResultSelector:
    def __init__(
        self,
        ext_name: str,
        data_req_with_prompts: list[tuple[DataCat, str|None]]
    ):
        self.ext_name = ext_name
        self.data_type = data_req_with_prompts
        self.check_result()
        self.n_res = len(self.data_type)
        self.layout_dict = dict()
        self.widgets_dict = dict()
        self.init_widget_dict()
        self.layout = self.init_layout()
    
    def init_widget_dict(self):
        self.widgets_dict["res_title"] = make_widget(Widget_type.div, text = f"<div style='font-size: 30px;'> Result")
        self.make_res_selections()

    def init_layout(self):
        res_key = ['res_title'] + [f"res_{i}" for i in range(self.n_res)]
        return make_layout(self.widgets_dict, res_key)
    
    def check_result(self):
        pass
    
    def make_res_selections(self):
        for i in range(self.n_res):
            self.widgets_dict[f"res_title_{i}"] = make_widget(Widget_type.div, text = f"<div style='font-size: 20px;'> {self.data_type[i][1]}")
            resultlist = self.find_result(i)
            self.widgets_dict[f"select_result_{i}"] = make_widget(
                Widget_type.select,
                lambda: self.res_selection_callback(),
                options = resultlist,
                value = resultlist[0]
            )
            self.widgets_dict[f"rename_{i}"] = make_widget(
                Widget_type.text,
                title = "Input new name for the result:"
            )
            self.widgets_dict[f"rename_name_confirm_{i}"] = make_widget(
                Widget_type.button,
                lambda: self.rename_confirm_callback(),
                label = "Name/Rename"
            )
            self.widgets_dict[f"mode_title_{i}"] = make_widget(Widget_type.div, text = "Select Save Mode")
            self.widgets_dict[f"mode_confirm_{i}"] = make_widget(
                Widget_type.radioButtonGroup,
                lambda: self.mode_confirm_callback(),
                labels = ["Create", "Replace", "Don't Save"],
                active = 0
            )
            self.widgets_dict[f"res_{i}"] = make_layout(
                self.widgets_dict, 
                [f"res_title_{i}", f"select_result_{i}", f"rename_{i}", f"rename_name_confirm_{i}", f"mode_title_{i}", f"mode_confirm_{i}"],
                LayoutOrientation.vertical
            )            

    def res_selection_callback(self):
        pass

    def res_confirm_callback(self):
        pass

    def rename_confirm_callback(self):
        pass

    def mode_confirm_callback(self):
        pass

    def find_result(
        self,
        i: int
    ):
        resultlist = [f"{self.data_type[i][1]}_{j}" for j in range(5)]
        return resultlist