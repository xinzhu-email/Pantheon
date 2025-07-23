from scpantheon.buttons import Widget_type, make_widget, make_layout
from scpantheon.base import Base
from scpantheon.widgets.modification import Modification


class Homepage():
    def __init__(self):
        self.widgets_dict = dict()
        self.layouts_dict = dict()
        self.init_widget_dict()
        self.layout = self.init_layout()
    
    def init_widget_dict(self):
        cell_title = make_widget(Widget_type.div, text = "<div style='font-size: 40px;'>Cell Based Visualization")
        cell_modification = Modification(Base.Cell)
        gene_title = make_widget(Widget_type.div, text = "<div style='font-size: 40px;'>Gene Based Visualization")
        gene_modification = Modification(Base.Gene)
        self.widgets_dict = {
            'cell_title': cell_title,
            'gene_title': gene_title,
            'cell_modification': cell_modification,
            'gene_modification': gene_modification
        }
    
    def init_layout(self):
        self.layouts_dict = {
            'cell_title': self.widgets_dict['cell_title'],
            'cell_modification': self.widgets_dict['cell_modification'].layout,
            'gene_title': self.widgets_dict['gene_title'],
            'gene_modification': self.widgets_dict['gene_modification'].layout
        }
        return(make_layout(self.layouts_dict))
