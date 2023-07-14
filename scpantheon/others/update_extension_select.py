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

import os, sys, io
import importlib
from PyQt5.QtWidgets import *
# import mysql.connector
from front_end import save_qt
from appdirs import AppDirs
import requests, zipfile, shutil

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

sys.path.append(str(Path(__file__).resolve().parents[1]))
try:
    from source import connection, plot_function
except:
    from scpantheon.source import connection, plot_function

color_list = d3['Category20c'][20]

####### SOURCE #######
def load_module(active):
    global extension_path
    plot = plot_function()
    buttons_group, buttons_n = plot.get_buttons_group() # buttons group, buttons number
    # delete last extended buttons
    for i in range(buttons_n, len(buttons_group)):
        buttons_group.pop()
    buttons = curdoc().get_model_by_name('module_buttons')
    try:
        name_list = os.listdir(extension_path)
    except:
        return     
    layouts = column()
    print('active:',active) # ex => active: Clustering_with_Scanpy
    ind = 0
    for name in name_list:
        but = curdoc().get_model_by_name(name)
        div = Div(text='')
        if name == active:
            sys.path.append(extension_path)
            module_name = name + '.module'
            try:
                new_class = module_name.new_layout()
            except:            
                mod = importlib.import_module(module_name) # usual way
                new_class = mod.new_layout()
            clear = Button(label='Clear the figures!', button_type='warning', name=str(ind))
            clear.on_click(lambda: clear_cb(clear.name))
            new_buttons = column(new_class.add(), clear)
            # append extended buttons
            buttons_group = find_buttons(new_buttons, buttons_group)
            plot.tweak_buttons_group(buttons_group)
            if but != None and but.visible == False:
                but.visible = True # already created model
                
                but.children.append(div)
                continue
            if but != None and but.visible == True:
                continue
            print('new_buttons:', new_buttons)
            new_buttons.sizing_mode = 'scale_height'
            new_buttons.name = name
            new_buttons.children.append(div)
            curdoc().add_root(new_buttons)
            layouts = column(layouts, new_buttons)

# D:\anaconda\Lib\site-packages\scpantheon\sourceqt.py
        else:
            if but != None:
                but.visible = False
        ind = ind + 1
    buttons = layouts
    if curdoc().get_model_by_name('module_buttons') == None:
        buttons.name = 'module_buttons'
    # curdoc().add_root(buttons)


###### Clustering with Scanpy ######
def pca():
    global buttons_group
    plot = plot_function()
    buttons_group, b = plot.get_buttons_group()
    button_disabled(buttons_group)
    def next_pca(buttons_group):
        layout = curdoc().get_model_by_name('Clustering_with_Scanpy')
        print(layout)
        change = connection()
        adata = change.get_anndata()

        sc.tl.pca(adata, svd_solver='arpack')
        sc.pl.pca_variance_ratio(adata, log=True, save='.png')

        img = open('figures/pca_variance_ratio.png','rb')
        img_base64 = base64.b64encode(img.read()).decode("ascii")
        div = Div(text="<img src=\'data:image/png;base64,{}\'/>".format(img_base64))
        layout.children.append(div)
        change.set_obsm(adata.obsm)
        button_abled(buttons_group)
    curdoc().add_next_tick_callback(lambda : next_pca(buttons_group))

def clear_cb(ind):
    module_checkbox = curdoc().get_model_by_name('modules_checkbox') 
    # options = module_checkbox.labels
    # for i in range(len(options)):
    #     if options[i] == 'Find_Marker_Gene':
    #         ind = i
    option = module_checkbox.value
    models = curdoc().get_model_by_name(option)
    curdoc().remove_root(models)
    print(curdoc().get_model_by_name(option))
    load_module(module_checkbox.value)