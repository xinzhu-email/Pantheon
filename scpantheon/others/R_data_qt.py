import os, sys
from PyQt5 import QtCore, QtGui
# import mysql.connector
from pathlib import Path
from appdirs import AppDirs
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

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

        RNA_path, ADT_file, Droplet_file = openreadtxt(dir)  
        self.text_brow.append('original RNA path:' + RNA_path + '\noriginal ADT path:' + ADT_file + '\noriginal Droplet path:' + Droplet_file + '\n') 


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