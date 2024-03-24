#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  2 19:25:32 2020

@author: lianqiuyu
"""

import pandas 
import argparse
import os
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
import sys
import base64
import anndata
from bokeh.models import ColumnDataSource, CDSView, IndexFilter, CustomJS, Circle, Div, Panel, Tabs, CheckboxGroup, FileInput,FixedTicker, ColorBar, LogColorMapper, Widget
from bokeh.palettes import d3
from bokeh.transform import log_cmap
from bokeh.layouts import row, column, layout
from bokeh.io import curdoc# current document
from bokeh.plotting import figure, output_file, save, show

filename = 'ADT.csv'

def parse_data():
    global data, dataplot, output_path
    # create parser
    parser = argparse.ArgumentParser()
    # add parameter
    parser.add_argument('--data_path',default='./data/'+filename,help = "The input path of CLR normalized data in .csv files with row as sample, col as feature.")
    print('./data/'+filename)
    # parser.add_argument('data_path',help = "The input path of CLR normalized data in .csv files with row as sample, col as feature.")
    parser.add_argument('-o', '--output', type=str, default='./CITEsort_out',help='Path to save output files.')
    parser.add_argument('--CLR', action='store_true', default=False, help='Input is raw counts. Transform counts into CLR format.')
    # parsing given parameter ?
    args = parser.parse_args()
    data_path = args.data_path

    if not os.path.exists(data_path):
        print('Error: input file does not exist. Please check.')
        sys.exit(0)

    # output default: './CITEsort_out'
    if args.output: 
        output_path = args.output
    else:
        output_path = "./CITEsort_out"

    if not os.path.exists(output_path):
        os.mkdir(output_path)

    print('read data.')
    data = pandas.read_csv(data_path,header=0,index_col=0)
    dataplot = data

    if args.CLR:
        print('perform CLR transformation on raw counts.')
        data_clr = np.apply_along_axis(lambda x: np.log(x+1) - np.mean(np.log(x+1)),0,data)
        data_clr = pandas.DataFrame(data_clr,index=data.index,columns = data.columns)
        data_clr.to_csv(output_path+'/data_clr.csv')
        dataplot = data_clr


def plt_plot(data):
    dataplot = data
    print('plot histgrams of all markers in CLR format.')
    # print('data.shape[0]:',data.shape[0], '\n[1]',data.shape[1])
    '''data.shape[0]: 15839 
    data.shape[1]: 10''' # the number of ADTs'

    plt.figure(figsize=(5.5,2*np.ceil(data.shape[1] / 5)), dpi=96) # / 5: 五列地行下去
            # width, height|天花板|     col           分辨率
    plt.style.use('seaborn-white')

    for i in range(dataplot.shape[1]): # 枚举列
        ax = plt.subplot(int(np.ceil(dataplot.shape[1] / 5)),5,i+1) # create height:2, width:5, index:i+1 subplot
        # subplot -> ax : Add an Axes to the current figure or retrieve an existing Axes.
        sns.distplot(dataplot.iloc[:,i].values,kde_kws={'bw':0.2})
        #         [row, col]|第i列|return array       估算数据密度 越小越拟合
        plt.yticks([0, 1]) # set -y axis range
        plt.title(dataplot.columns[i],fontsize=7)
        if i%5 == 0:
            plt.ylabel('Density',fontsize=5.5)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False) # 去掉右、下边图框
        ax.yaxis.set_ticks_position('left')

    plt.suptitle('DB: '+str(dataplot.shape[1])+' ADTs, '+str(dataplot.shape[0])+' droplets',fontsize=7)    
    plt.subplots_adjust(top=0.9, bottom=0.1, left=0.1, right=0.9, hspace=0.6,wspace=0.15) 
    #                   坐标作为表现 bottom <= top                 垂直间距    水平间距
    #plt.subplots_adjust(top=0.85)
    #plt.savefig('./PBMC_16k/marker_hist.png')
    plt.savefig(output_path+'/data_cls_hist.png')
    plt.clf()


def pca():
    global data, output_path
    #layout = curdoc().get_model_by_name('Show_plot')
    #print('=====',layout,'=====')
    parse_data()
    plt_plot(data=data)
    img = open(output_path+'/data_cls_hist.png','rb')
    img_base64 = base64.b64encode(img.read()).decode("ascii")
    div = "<img src=\'data:image/png;base64,{}\'/>".format(img_base64)
    #layout.text = div
