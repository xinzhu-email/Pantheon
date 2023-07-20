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

data_file = 'C:/Users/23606/Documents/Workspace/Pantheon/scpantheon/data/adt_t.csv'
adata = sc.read_csv(data_file) 

print(adata)
print(adata.obs.info())
print(adata.var.info())
print(adata.obsm)