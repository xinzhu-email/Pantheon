import os
import scanpy as sc
from io import BytesIO
from bokeh.palettes import d3
import json
import base64
import sys
from pathlib import Path
from bokeh.io import curdoc
from bokeh.models import FileInput, Button, TextInput, Div, Select
from bokeh.layouts import row, column
import pandas
import numpy as np

sys.path.append(str(Path(__file__).resolve().parents[1]))
try:
    from source import connection, plot_function
except:
    from scpantheon.source import connection, plot_function

class new_layout:
    def __init__(self):
        self.new_button = Button(label='Show Histogram')
        self.new_button.on_click(check_histogram) 
    
    def add(self):
        return self.new_button

def check_histogram():
    layout = curdoc().get_model_by_name('Check_Histogram')
    change = connection()
    data_file = change.get_data_file()
    pdata = pandas.read_csv(data_file, index_col=0)
    plot = plot_function()
    p = plot.get_figure()


    # pdata[self.data_columns[x_init_idx]].describe()

    '''the column won't change as the view changes
    still bugs..'''
    hist, edges = np.histogram(pdata[column[0]],bins = int(10/0.05),range = [0, 10])
    hist2, edges2 = np.histogram(pdata[column[1]],bins = int(10/0.05),range = [0, 10])
    amount = pandas.DataFrame({'pdata': np.log(hist),'left': edges[:-1],'right': edges[1:]})
    amount2 = pandas.DataFrame({'pdata': np.log(hist2),'left': edges2[:-1],'right': edges2[1:]})
    q1 = p.quad(bottom=0,top=amount['pdata'],left=amount['left'],right=amount['right'],line_color=None,fill_color="#c3f4b2",fill_alpha=0.3,legend_label='qx')
    l1 = p.line(x=np.linspace(0, 10, 200), y=amount['pdata'], line_color="#3333cc", line_width=2, alpha=0.3, legend_label="lx")
    q2 = p.quad(bottom=amount2['left'],top=amount2['right'],left=0,right=amount2['pdata'],line_color=None,fill_color='#FFC125',fill_alpha=0.3,legend_label='qy')
    l2 = p.line(x=amount2['pdata'], y=np.linspace(0, 10, 200), line_color="#ff8888", line_width=2, alpha=0.3, legend_label="ly")
    p.legend.location = "center_right"
    p.legend.click_policy = "hide"