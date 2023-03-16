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

sys.path.append(str(Path(__file__).resolve().parents[1]))
try:
    from source import connection, plot_function
except:
    from scpantheon.source import connection, plot_function

class new_layout:
    def __init__(self):
        global buttons_group
        self.show_button = Button(label='Show Histogram')
        self.show_button.on_click(check_histogram) 
        self.remove_button = Button(label='Remove')
        self.remove_button.on_click(remove)

    def add(self):
        return column(self.show_button, 
                      self.remove_button)

def button_disabled(buttons_group):
    for b in buttons_group:
        b.disabled = True

def button_abled(buttons_group):
    for b in buttons_group:
        b.disabled = False

def check_histogram():
    global buttons_group

    plot = plot_function()
    buttons_group, b = plot.get_buttons_group() # group and the original amount
    button_disabled(buttons_group)
    def next_check():
        global plotlist, p, glylist
        layout = curdoc().get_model_by_name('Check_Histogram')
        change = connection()
        #pdata = change.get_pandata()
        adata = change.get_anndata()
        plot = plot_function()
        p = plot.get_figure()
        x, y = plot.get_x_y()
        glylist = plot.get_glyph_list()

        # get the x and y of plot
        cnt = 0
        for axis in adata.var.index:
            if(x == axis): x = cnt
            if(y == axis): y = cnt
            cnt += 1
        
        def ad_to_pd():
            global pdata
            X = adata.X
            obs_df = adata.obs
            var_df = adata.var
            pdata = pandas.concat([obs_df, var_df, pandas.DataFrame(X.T)], axis=1)
            pdata = pdata.T
        ad_to_pd()

        if len(glylist) <= 1:
            # pdata[self.data_columns[x_init_idx]].describe()
            hist, edges = np.histogram(pdata[x],bins = int(10/0.05),range = [0, 10])
            hist2, edges2 = np.histogram(pdata[y],bins = int(10/0.05),range = [0, 10])
            amount = pandas.DataFrame({'pdata': np.log(hist),'left': edges[:-1],'right': edges[1:]})
            amount2 = pandas.DataFrame({'pdata': np.log(hist2),'left': edges2[:-1],'right': edges2[1:]})
            q1 = p.quad(bottom=0,top=amount['pdata'],left=amount['left'],right=amount['right'],line_color=None,fill_color="#c3f4b2",fill_alpha=0.3,legend_label='qx')
            l1 = p.line(x=np.linspace(0, 10, 200), y=amount['pdata'], line_color="#3333cc", line_width=2, alpha=0.3, legend_label="lx")
            q2 = p.quad(bottom=amount2['left'],top=amount2['right'],left=0,right=amount2['pdata'],line_color=None,fill_color='#FFC125',fill_alpha=0.3,legend_label='qy')
            l2 = p.line(x=amount2['pdata'], y=np.linspace(0, 10, 200), line_color="#ff8888", line_width=2, alpha=0.3, legend_label="ly")
            plotlist = [q1, q2, l1, l2]
            glylist.extend(plotlist)
            p.legend.location = "center_right"
            p.legend.click_policy = "hide"
        else:
            print('Histogram already existed')
        button_abled(buttons_group)
    curdoc().add_next_tick_callback(next_check)


def remove():
    global glylist
    button_disabled(buttons_group)
    def next_remove():
        if len(glylist) > 1:
            for plot in plotlist:
                glylist.remove(plot)
        else:
            print('Histogram already deleted')
        for glygh in plotlist:
            try:
                p.renderers.remove(glygh)
            except: print('no glyph')
            button_abled(buttons_group)
    curdoc().add_next_tick_callback(next_remove)
