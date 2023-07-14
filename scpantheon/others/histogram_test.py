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
import pandas, anndata
import numpy as np
import json
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, CustomJS, Circle, Div, Panel, Tabs, CheckboxGroup, FileInput,FixedTicker, ColorBar, LogColorMapper, Widget, Quad
from bokeh.models.widgets import Select, Button, ColorPicker,TextInput, DataTable, MultiSelect, AutocompleteInput
from bokeh.events import ButtonClick
from bokeh.transform import log_cmap
from bokeh.palettes import d3
from bokeh.layouts import row, column, layout
from bokeh.io import curdoc# current document
from bokeh.plotting import figure, output_file, save, show
from bokeh.embed import components, file_html
from bokeh.resources import CDN
import pandas 
import numpy as np
import anndata
import scipy.sparse as ss
import colorcet as cc
import scanpy as sc
# from new_func import new_layout
# from main3 import change_class_color

import os, sys
import importlib
from PyQt5.QtWidgets import *
# import mysql.connector
from appdirs import AppDirs



data_file = 'C:/Users/23606/Documents/Workspace/Pantheon/scpantheon/data/adt_t.csv'
filename = os.path.split(data_file)[1]  
filetype = os.path.splitext(data_file)[-1][1:] # split the filename and the type
                                                      # [-1] means the last tuple: the type 
if filetype == 'csv':
    adata = sc.read_csv(data_file) 
    print('csv')
elif filetype == 'h5ad':
    # adata = sc.read_h5ad(data_file)
    adata = anndata.read(data_file, backed='r')
    print('h5ad')
elif filetype == 'mtx':
    adata = sc.read_10x_mtx(
        'data/hg19/',  # the directory with the `.mtx` file
        var_names='gene_symbols',                # use gene symbols for the variable names (variables-axis index)
        cache=True)                              # write a cache file for faster subsequent reading

def ad_to_pd():
    global pdata
    X = adata.X
    obs_df = adata.obs
    var_df = adata.var
    pdata = pandas.concat([obs_df, var_df, pandas.DataFrame(X.T)], axis=1)
    pdata = pdata.T
ad_to_pd()

df = adata.to_df()
dl = np.log1p(df)
data_columns = df.columns.values.tolist()


'''for c in data_columns:
    print(c)'''

'''for x in df[data_columns[0]]:
    if x == 0:
        print(x)'''

'''for row in pdata.iterrows():
    for x in row:
        print(x)'''
TOOLTIPS = [
        ("(x,y)", "($x, $y)"),
        ("color", "@color"),
]
p = figure(width=500, height=500, tools="pan,lasso_select,box_select,tap,wheel_zoom,save,hover",title="sf", tooltips=TOOLTIPS, output_backend="webgl")
# max_range = pdata.max().max()
# median_range = pdata.median().median()
# mean_range = pdata.mean().mean()
# pdata[self.data_columns[x_init_idx]].describe()
mean_range = np.mean(adata.X)

# Show log data according to the checkbox log_axis
log_axis = plot.get_log_axis()
def get_df_x_y(df, mean_range):
    if log_axis.active == []:
        df_x = df[x]
        df_y = df[y]
        mean_range = mean_range
    else:
        df_x = np.log1p(df[x])
        df_y = np.log1p(df[y])
        mean_range = np.log1p(mean_range)
        # if mean_range < 200: mean_range = 200
    return df_x, df_y, mean_range

# Numpy for data modeling
bins = np.linspace(0, int(mean_range * 6), int(5e4))
try:
    df = change.get_data_df()
except:
    df = adata.to_df()
df_x, df_y, mean_range = get_df_x_y(df, mean_range)
# print('mean_range\n', mean_range)
# print('hist:\n', hist)
hist, edges = np.histogram(df_x, bins = bins, range = [0, mean_range * 6])
hist2, edges2 = np.histogram(df_y, bins = bins, range = [0, mean_range * 6])
'''q1 = p.quad(bottom=0,top=np.log1p(hist),left=edges[:-1],right=edges[1:],line_color=None,fill_color="#c3f4b2",fill_alpha=0.3,legend_label='qx')
l1 = p.line(x=np.linspace(0, mean_range * 3, int(mean_range)), y=np.log1p(hist), line_color="#3333cc", line_width=2, alpha=0.3, legend_label="lx")
q2 = p.quad(bottom=edges2[:-1],top=edges2[1:],left=0,right=np.log1p(hist2),line_color=None,fill_color='#FFC125',fill_alpha=0.3,legend_label='qy')
l2 = p.line(x=np.log1p(hist2), y=np.linspace(0, mean_range * 3, int(mean_range)), line_color="#ff8888", line_width=2, alpha=0.3, legend_label="ly")'''
# bins = np.linspace(0, int(mean_range * 6), int(1e4))
q1 = p.quad(bottom=0,top=hist,left=edges[:-1],right=edges[1:],line_color="#3333cc",fill_color="#c3f4b2",fill_alpha=0.3,legend_label='qx')
# l1 = p.line(x=bins, y=hist, line_color="#3333cc", line_width=2, alpha=0.3, legend_label="lx")
q2 = p.quad(bottom=edges2[:-1],top=edges2[1:],left=0,right=hist2,line_color="#ff8888",fill_color='#FFC125',fill_alpha=0.3,legend_label='qy')
# l2 = p.line(x=hist2, y=bins, line_color="#ff8888", line_width=2, alpha=0.3, legend_label="ly")
# plotlist = [q1, q2, l1, l2]
plotlist = [q1, q2]
p.legend.location = "center_right"
p.legend.click_policy = "hide"