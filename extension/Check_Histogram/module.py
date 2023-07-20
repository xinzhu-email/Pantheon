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
from scpantheon import source as soc

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
    plot = soc.plot_function()
    buttons_group, b = plot.get_buttons_group() # group and the original amount
    button_disabled(buttons_group)
    def next_hist(buttons_group):
        global plotlist, p, glylist
        '''for b in buttons_group:
            print(b.disabled)'''
        layout = curdoc().get_model_by_name('Check_Histogram')
        change = soc.connection()
        #pdata = change.get_pandata()
        adata = change.get_anndata()
        plot = soc.plot_function()
        p = plot.get_figure()
        x, y = plot.get_x_y()
        print('x:', x, '\ny:', y)
        glylist = plot.get_glyph_list()
        # adata.obsm = change.get_obsm()
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
            bins = np.linspace(0, int(mean_range * 6), int(1e4))
            try:
                df = change.get_data_df()
            except:
                df = adata.to_df()
            df_x, df_y, mean_range = get_df_x_y(df, mean_range)
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
