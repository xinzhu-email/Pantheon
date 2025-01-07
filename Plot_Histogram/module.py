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
from scipy.stats import gaussian_kde

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scpantheon import source as soc

class new_layout:
    def __init__(self):
        global buttons_group
        show_button = Button(label='Show Histogram')
        show_button.on_click(plot_histogram) 
        remove_button = Button(label='Remove')
        remove_button.on_click(remove)
        self.de = column(show_button, 
                        remove_button)


    def add(self):
        return self.de

def button_disabled(buttons_group):
    for b in buttons_group:
        b.disabled = True

def button_abled(buttons_group):
    for b in buttons_group:
        b.disabled = False

def plot_histogram():
    global buttons_group
    plot = soc.plot_function()
    buttons_group, b = plot.get_buttons_group() # group and the original amount
    button_disabled(buttons_group)
    def next_hist(buttons_group):
        global plotlist, p, glylist
        '''for b in buttons_group:
            print(b.disabled)'''
        # layout = curdoc().get_model_by_name('Check_Histogram')
        change = soc.connection()
        #pdata = change.get_pandata()
        adata = change.get_anndata()
        plot = soc.plot_function()
        p = plot.get_figure()
        x, y = plot.get_x_y()
        print('x:', x, '\ny:', y)
        glylist = plot.get_glyph_list()

        if len(glylist) <= 1:
            log_axis = plot.get_log_axis()
            def get_df_x_y(df):
                if log_axis.active == []:
                    df_x = df[x]
                    df_y = df[y]
                else:
                    df_x = np.log1p(df[x])
                    df_y = np.log1p(df[y])
                return df_x, df_y

            try:
                df = change.get_data_df()
            except:
                df = adata.to_df()
            df_x, df_y = get_df_x_y(df)
            density1, density2 = gaussian_kde(df_x), gaussian_kde(df_y)
            x1 = np.linspace(min(df_x), max(df_x), 100)  
            y1 = density1(x1) 
            x2 = np.linspace(min(df_y), max(df_y), 100) 
            y2 = density2(x2) 
            max_x1 = max(x1)
            max_x2 = max(x2)
            # y normalization
            y2 = y2 / max(y2) * max_x1
            y1 = y1 / max(y1) * max_x2

<<<<<<< HEAD
=======
            # print("new extension")
>>>>>>> extension
            #   
            d1 = p.line(x1, y1, line_color="#00CCCC", line_width=2, legend_label = "d1")
            p1 = p.patch(np.append(x1, x1[::-1]), np.append(y1, np.zeros_like(y1)), color="#99d8c9", alpha=0.4, legend_label = "p1")
            #  #FF99FF   #FF9999   |    #6699FF   #99CCFF
            d2 = p.line(y2, x2, line_color="#FF9999", line_width=2, legend_label = "d2")
            p2 = p.patch(np.append(y2, y2[::-1]), np.append(x2, np.zeros_like(x2)), color="#FF99FF", alpha=0.4, legend_label = "p2")
            plotlist = [d1, d2, p1, p2]
            glylist.extend(plotlist)
            p.legend.location = "center_right"
            p.legend.click_policy = "hide"
            '''
            # print('mean_range\n', mean_range)
            # print('hist:\n', hist)
            hist, edges = np.histogram(df_x, bins = bins, range = [0, mean_range * 6])
            hist2, edges2 = np.histogram(df_y, bins = bins, range = [0, mean_range * 6])
            q1 = p.quad(bottom=0,top=hist,left=edges[:-1],right=edges[1:],line_color="#65E627",line_alpha=0.3,fill_color="#c3f4b2",fill_alpha=0.1,legend_label='qx')
            # l1 = p.line(x=bins, y=hist, line_color="#3333cc", line_width=2, alpha=0.3, legend_label="lx")
            q2 = p.quad(bottom=edges2[:-1],top=edges2[1:],left=0,right=hist2,line_color="#E6B666",line_alpha=0.3,fill_color='#FFC125',fill_alpha=0.1,legend_label='qy')
            # l2 = p.line(x=hist2, y=bins, line_color="#ff8888", line_width=2, alpha=0.3, legend_label="ly")
            # plotlist = [q1, q2, l1, l2]
            plotlist = [q1, q2]
            glylist.extend(plotlist)
            p.legend.location = "center_right"
            p.legend.click_policy = "hide"
            '''
        else:
            print('Histogram already existed')
        button_abled(buttons_group)
    curdoc().add_next_tick_callback(lambda : next_hist(buttons_group))


def remove():
    global glylist
    button_disabled(buttons_group)
    def next_remove(glylist):
        '''for b in buttons_group:
            print(b.disabled)'''
        if len(glylist) > 1:
            for plot in plotlist:
                glylist.remove(plot)
        else:
            print('Histogram already deleted')
        for glygh in plotlist:
            try:
                p.renderers.remove(glygh)
            except: print('no graph')
        button_abled(buttons_group)
    curdoc().add_next_tick_callback(lambda : next_remove(glylist))
