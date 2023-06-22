from bokeh.models import Button
import json
import sys
from pathlib import Path
from bokeh.io import curdoc

sys.path.append(str(Path(__file__).resolve().parents[1]))
try:
    from source import connection, plot_function
except:
    from scpantheon.source import connection, plot_function

class new_layout:
    def __init__(self):
        self.new_button = Button(label='Change Color')
        self.new_button.on_click(change_color) 
    
    def add(self):
        return self.new_button
    

def button_disabled(buttons_group):
    for b in buttons_group:
        b.disabled = True

def button_abled(buttons_group):
    for b in buttons_group:
        b.disabled = False


def change_color(): 
    global buttons_group

    plot = plot_function()
    buttons_group, b = plot.get_buttons_group()
    button_disabled(buttons_group)
    def next_color(buttons_group):
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
        button_abled(buttons_group)
    curdoc().add_next_tick_callback(lambda : next_color(buttons_group))