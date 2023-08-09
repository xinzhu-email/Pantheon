from pickletools import optimize
import scanpy as sc
from io import BytesIO
from bokeh.palettes import d3
import json
import base64
import sys
from pathlib import Path
from bokeh.io import curdoc
from bokeh.models import FileInput, Button, TextInput, Div, Select, MultiChoice
from bokeh.layouts import row, column
from appdirs import AppDirs
import os, sys
from PyQt5 import QtCore, QtGui
from pathlib import Path
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import rpy2.robjects as ro

sys.path.append(str(Path(__file__).resolve().parents[1]))
from scpantheon import source as soc
# from scpantheon.front_end import R_data_qt

r = ro.r

class new_layout:
    def __init__(self):
        # assay_list <<- Assays(new_data)
        r('''
            library(Seurat)
            library(Matrix)
            library(cowplot)
            library(dplyr)
            library(magick)
            library(gridExtra)

            # read data
            read_mtx <- function(mtx_folder){
                sp_matrix_read <- readMM(file.path(mtx_folder,"matrix.mtx.gz"))
                features = read.table(file.path(mtx_folder,"features.tsv.gz"))
                barcodes = read.table(file.path(mtx_folder,"barcodes.tsv.gz"))
                if(ncol(features)>1){
                    sp_matrix_read@Dimnames[[1]] = features[,2]
                }else{
                    sp_matrix_read@Dimnames[[1]] = features[,1]
                }
                sp_matrix_read@Dimnames[[2]] = barcodes[,1]
                new_data <<- CreateSeuratObject(counts = sp_matrix_read, assay='RNA')
            }

            read_csv <- function(file_path){
                new_label <<- read.csv(file_path)
            }

            Create_data_adt <- function(file){
                new_data.adt <<- as.sparse(t(read.csv(file = file, sep = ",",header = TRUE, row.names = 1)))
                new_data.adt <<- CreateAssayObject(counts = new_data.adt)
                new_data[['ADT']] <<- new_data.adt
            }

        ''')

        folder_file_button = Button(label = 'Choose RNA folder, ADT file and Droplet', button_type = 'success')
        folder_file_button.on_click(lambda : get_data_r_init())

        # reduction = TextInput(title = 'reduction method:', value = 'pca')
        # resolution = TextInput(title = 'resolution value:', value = '1')
        # dims = TextInput(title = 'dims value(1:?): ', value = '30')
        # nn = TextInput(title = 'nn.name:', value = '')
        # assay = Select(title = 'Select assay:', options = assay_list, value = 'RNA')
        # assay = TextInput(title = 'assay value:', value = 'RNA')
        R_umap_plot = Button(label = 'Plot R UMAP', button_type = 'success')
        R_umap_plot.on_click(lambda: plot_r_umap())

        self.R_map = column(folder_file_button,
                        # row(assay, resolution),
                        R_umap_plot)

    def add(self):
        return self.R_map


def button_disabled(buttons_group):
    for b in buttons_group:
        b.disabled = True

def button_abled(buttons_group):
    for b in buttons_group:
        b.disabled = False


def plot_r_umap():
    global buttons_group

    plot = soc.plot_function()
    buttons_group, b = plot.get_buttons_group()
    button_disabled(buttons_group)
    def plot_r(buttons_group):
        r('''
            DefaultAssay(new_data) <- 'RNA' 
            new_data <- NormalizeData(new_data) %>% FindVariableFeatures() %>% ScaleData() %>% RunPCA()
            DefaultAssay(new_data) <- 'ADT'
            VariableFeatures(new_data) <- rownames(new_data[["ADT"]])
            new_data <- NormalizeData(new_data, normalization.method = 'CLR', margin = 2) %>% ScaleData() %>% RunPCA(reduction.name = 'apca')
            new_data <- FindMultiModalNeighbors(new_data, reduction.list = list("pca", "apca"), dims.list = list(1:30, 1:18), modality.weight.name = "RNA.weight")
            new_data <- RunUMAP(new_data, nn.name = "weighted.nn", reduction.name = "wnn.umap", reduction.key = "wnnUMAP_")
        ''')
        r('''
            new_data@meta.data['label'] <- new_label[,'cell_type']
            new_data <- FindClusters(new_data, graph.name = "wsnn", algorithm = 3, resolution = 1, verbose = FALSE)

            p1 <- DimPlot(new_data, reduction = 'wnn.umap', label = TRUE, repel = TRUE, label.size = 2.5) + NoLegend()
            p2 <- DimPlot(new_data, reduction = 'wnn.umap', group.by='label', label = TRUE, repel = TRUE, label.size = 2.5) + NoLegend()
            p1+p2
        ''')
        r('''
            png(filename = "p1+p2.png", width = 10, height = 6, units = "in", res = 300)
            print(plot_grid(p1, p2, ncol = 2))
            dev.off()
        ''')
        button_abled(buttons_group)
    curdoc().add_next_tick_callback(lambda : plot_r(buttons_group))

    
def get_data_r_init():
    global buttons_group

    plot = soc.plot_function()
    buttons_group, b = plot.get_buttons_group()
    button_disabled(buttons_group)
    def get(buttons_group):
        global RNA_folder, ADT_file, Droplet_file
        if main() == 'app closed':
            print('choosing finished')
        appname = "scpantheon"
        appauthor = "xinzhu"
        version = "0.2.1"
        dirs = AppDirs(appname, appauthor, version)
        dir = dirs.user_data_dir
        RNA_folder, ADT_file, Droplet_file = openreadtxt(dir) 
        r['read_mtx'](RNA_folder)
        r['Create_data_adt'](ADT_file)
        r['read_csv'](Droplet_file)
        button_abled(buttons_group)
    curdoc().add_next_tick_callback(lambda : get(buttons_group))


def openreadtxt(dir):
    rna_file = open(dir + '/' + 'RNA_folder.txt', 'r')
    rna_path = rna_file.readline()
    rna_file.close()
    print('rna path:', rna_path)
    adt_file = open(dir + '/' + 'ADT_file.txt', 'r')
    adt_path = adt_file.readline()
    print('adt path:', adt_path)
    droplet_file = open(dir + '/' + 'Droplet_file.txt', 'r')
    droplet_path = droplet_file.readline()
    print('droplet file:', droplet_path)
    droplet_file.close()
    return rna_path, adt_path, droplet_path



sys.path.append(str(Path(__file__).resolve().parents[1]))

class Ui_Dialog(QDialog, QWidget, object):
    my_signal = pyqtSignal(str)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Choose")
        Dialog.resize(750, 900)
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)

        # render help text
        self.text_brow = QTextBrowser()

        '''
        folder:
        RNA_folder
        file:
        ADT_file
        Droplet_file
        '''

        # folder
        self.btn_RNA_folder = QPushButton("RNA_folder",self)  
        self.btn_RNA_folder.setObjectName("btn_RNA_folder")  
        self.btn_RNA_folder.clicked.connect(self.slot_RNA_folder)
        self.btn_RNA_folder.setFont(font)
        self.btn_RNA_folder.setMinimumSize(750, 100)
        # self.btn_Extensions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # file1
        self.btn_ADT_file = QPushButton("ADT_file",self)  
        self.btn_ADT_file.setObjectName("btn_ADT_file")  
        self.btn_ADT_file.clicked.connect(self.slot_ADT_file)
        self.btn_ADT_file.setFont(font)
        self.btn_ADT_file.setMinimumSize(750, 100)
        # self.btn_Data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # file2
        self.btn_Droplet_file = QPushButton("Droplet_file",self)  
        self.btn_Droplet_file.setObjectName("btn_Droplet_file")  
        self.btn_Droplet_file.clicked.connect(self.slot_Droplet_file)
        self.btn_Droplet_file.setFont(font)
        self.btn_Droplet_file.setMinimumSize(750, 100)

        # folder
        self.btn_RNA_folder = QPushButton("RNA_folder",self)
        self.btn_RNA_folder.setObjectName("btn_RNA_folder")
        self.btn_RNA_folder.clicked.connect(self.slot_RNA_folder)
        self.btn_RNA_folder.setFont(font)
        self.btn_RNA_folder.setMinimumSize(750, 100)
        # self.btn_Start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout(Dialog)
        self.layout2.setObjectName("Layout2")    
        self.layout2.addWidget(self.text_brow)             

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setObjectName("buttonBox")
        self.layout2.addWidget(self.buttonBox)

        self.layout2.addWidget(self.btn_ADT_file)
        self.layout2.addWidget(self.btn_Droplet_file)
        self.layout2.addWidget(self.btn_RNA_folder)

        # self.retranslateUi(Dialog) 
        # self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        try:
            RNA_path, ADT_file, Droplet_file = openreadtxt(dir)  
            self.text_brow.append('original RNA path:' + RNA_path + '\noriginal ADT path:' + ADT_file + '\noriginal Droplet path:' + Droplet_file + '\n') 
        except:
            print('path not exist')

    def event(self, event):
        if event.type()==QtCore.QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            self.text_brow.setText("Choose your extension packages and your data") 
        return QDialog.event(self,event)

    def slot_RNA_folder(self):
        global RNA_folder
        RNA_folder = QFileDialog.getExistingDirectory(self,"Choose RNA folder",self.cwd) # 起始路径
        if RNA_folder == "":
            print("\nchoose canceled")
            return

        # write extension into user_data_dir
        text_create('RNA_folder', RNA_folder)
        print("\RNA folder:",RNA_folder)
        self.text_brow.append("new RNA folder:" + RNA_folder)

    def slot_ADT_file(self):
        global ADT_file
        ADT_file, file_type = QFileDialog.getOpenFileName(self,"Choose ADT file", self.cwd)   # 设置文件扩展名过滤,用双分号间隔

        if ADT_file == "":
            print("\nchoose canceled")
            return

        # write Data into user_data_dir
        text_create('ADT_file', ADT_file)
        print("\nADT:",ADT_file)
        self.text_brow.append("new ADT path:" + ADT_file)

    def slot_Droplet_file(self):
        global Droplet_file
        Droplet_file, file_type = QFileDialog.getOpenFileName(self,"Choose Droplet file", self.cwd)   # 设置文件扩展名过滤,用双分号间隔

        if Droplet_file == "":
            print("\nchoose canceled")
            return

        # write Data into user_data_dir
        text_create('Droplet_file', Droplet_file)
        print("\Droplet:",Droplet_file)
        self.text_brow.append("new Droplet path:" + Droplet_file)

    def rejected(self, Dialog):
        Dialog.reject()
        check_code = 'app closed'
        self.my_signal.emit(check_code)


    '''def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Choose", "Choose"))'''


def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print(path + ' successful creat')
        return True
    else:
        print(path + ' already exist')


def text_create(name, msg):
    path = dir + "/" + name + '.txt'
    print("-========- path:", path)
    with open(path, "w") as f:
        f.truncate(0)
        f.close()
    file = open(path, 'w')
    file.write(msg)
    file.close()


def openreadtxt(dir):
    rna_file = open(dir + '/' + 'RNA_folder.txt', 'r')
    rna_path = rna_file.readline()
    rna_file.close()
    print('rna path:', rna_path)
    adt_file = open(dir + '/' + 'ADT_file.txt', 'r')
    adt_path = adt_file.readline()
    print('adt path:', adt_path)
    droplet_file = open(dir + '/' + 'Droplet_file.txt', 'r')
    droplet_path = droplet_file.readline()
    print('droplet file:', droplet_path)
    droplet_file.close()
    return rna_path, adt_path, droplet_path


def signal_slot(data):
    global check_code
    # print("check code:", data)
    check_code = data


def main():
    global dir
    # create the file to write data
    appname = "scpantheon"
    appauthor = "xinzhu"
    version = "0.2.1"
    dirs = AppDirs(appname, appauthor, version)
    dir = dirs.user_data_dir
    mkdir(path=dir)
    # create qt app
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    ui.my_signal.connect(signal_slot)
    Dialog.show()
    app.exec()
    try: return check_code
    except: return 'app ended'

# 利用'app closed' 使 X 是关闭