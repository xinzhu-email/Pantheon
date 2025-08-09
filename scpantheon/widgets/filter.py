from scpantheon.buttons import Widget_type, make_widget, make_layout
from scpantheon.base import Base
from scpantheon.stdata import DataCat
from scpantheon.tabs import refresh

class Filter:
    def __init__(self, base: Base):
        self.base = base
        self.widgets_dict = self.init_widget_dict()
        self.layout = self.init_layout()
    
    def init_widget_dict(self):
        filter_title = make_widget(Widget_type.div, text = f"<div style='font-size: 30px;'> {self.base.value} Selection")
        filter_mode = make_widget(
            Widget_type.select, 
            lambda: self.filter_mode_callback(), 
            options = ['Filter by Value', 'Filter by Selected Groups', 'Filter by Manual Selection'],
            value = 'Filter by Selected Groups'
            )
        val_options = self.get_val_options()
        type_values = [member.value for member in DataCat]
        variable_type = make_widget(
            Widget_type.select, 
            lambda: self.variable_type_callback(), 
            options = type_values, 
            value = type_values[0], 
            title = "select variable type: "
            )
        variable = make_widget(
            Widget_type.select, 
            lambda: self.variable_callback(), 
            options = val_options, 
            value = val_options[0], 
            title = "filter by variable: "
            )
        rangemin = make_widget(Widget_type.text, lambda: self.range_callback("min"), title = "min value")
        rangemax = make_widget(Widget_type.text, lambda: self.range_callback("max"), title = "max value")
        return {
            'filter_title': filter_title,
            'filter_mode': filter_mode,
            'variable': variable,
            'variable_type': variable_type,
            'rangemin': rangemin,
            'rangemax': rangemax
        }

    def init_layout(self):
        fixed_key = ['filter_title', 'filter_mode']
        if self.widgets_dict['filter_mode'].value == 'Filter by Value':
            filter_key = ['variable_type', 'variable', 'rangemin', 'rangemax']
        else:
            filter_key = []
        self.change_layout = make_layout(self.widgets_dict, filter_key)
        self.fixed_layout = make_layout(self.widgets_dict, fixed_key)
        return make_layout([self.fixed_layout, self.change_layout])
    
    def filter_mode_callback(self):
        fresh_id = self.change_layout.id
        if self.widgets_dict['filter_mode'].value == 'Filter by Value':
            filter_key = ['variable_type', 'variable', 'rangemin', 'rangemax']
        else:
            filter_key = []
        self.change_layout = make_layout(self.widgets_dict, filter_key)
        refresh(fresh_id, self.change_layout)
    
    def variable_type_callback(self):
        pass
    
    def variable_callback(self):
        pass

    def range_callback(self):
        pass
    
    def group_callback(self):
        pass

    def cluster_callback(self):
        pass

    def get_val_options(self):
        return ['value variable 0']