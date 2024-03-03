import os, sys
from PyQt5 import QtCore, QtGui
# import mysql.connector
from pathlib import Path
from appdirs import AppDirs
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from scpantheon.front_end.data_qt import dir

sys.path.append(str(Path(__file__).resolve().parents[1]))

try:
    from scpantheon.front_end.data_qt import write_msg, mkdir
except: 
    from data_qt import write_msg, mkdir

class Ui_Dialog(QDialog, QWidget, object):
    my_signal = pyqtSignal(str)

    def __init__(self):
        super(Ui_Dialog, self).__init__()
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Online Package Loader")
        Dialog.resize(750,300)
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)

        # render help text
        self.text_brow = QTextBrowser()

        # choose path button
        self.btn_download = QPushButton("Choose New Loading Path", self)  
        self.btn_download.setObjectName("btn_download")  
        self.btn_download.clicked.connect(self.slot_btn_download)
        self.btn_download.setFont(font)
        self.btn_download.setMinimumSize(750, 100)

        # Start load
        self.btn_Start = QPushButton("Loading Path Not Found",self)
        self.btn_Start.setObjectName("btn_Start")
        self.btn_Start.clicked.connect(lambda : self.Load(Dialog))
        self.btn_Start.setFont(font)
        self.btn_Start.setMinimumSize(750, 100)
        
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout(Dialog)
        self.layout2.setObjectName("Layout2")    
        self.layout2.addWidget(self.text_brow)             

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setObjectName("buttonBox")
        self.layout2.addWidget(self.buttonBox)

        self.layout2.addWidget(self.btn_download)
        self.layout2.addWidget(self.btn_Start)

        # self.retranslateUi(Dialog) 
        # self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        load_path = get_load_path()
        if load_path != '':
            self.btn_Start.setText("Load Packages In The Previous Path")
            self.text_brow.setText("\t\t\tPrevious Loading Path:\n\t" + load_path)
        else:
            self.btn_download.setText("Choose A Loading Path!")
            self.text_brow.setText("\t\t\tLoading Path Not Found...")
        # self.text_brow.append('original output path:' + output_path) 

    def event(self, event):
        if event.type()==QtCore.QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            # self.text_brow.setText("Choose the path to load your file")
        return QDialog.event(self,event)

    def slot_btn_download(self):
        load = QFileDialog.getExistingDirectory(self,"Choose load",self.cwd) # 起始路径
        # write extension into user_data_dir
        if load != '':
            write_msg('load_path', load)

    def Load(self, Dialog):
        global check_code
        check_code = 'app closed'
        Dialog.reject()

def get_load_path():
    l_file = open(dir + '/' + 'load_path.txt', 'r')
    l_path = l_file.readline()
    l_file.close()
    # print('-======- load_path', l_path)
    return l_path


def main():
    global check_code
    check_code = "app_running"
    mkdir(path=dir)
    # create qt app
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  
    Dialog.show()
    app.exec()
    return check_code
 
'''def write_msg(name, msg):
    path = dir + "/" + name + '.txt'
    # print("-========- path:", path)
    with open(path, "w") as f:
        f.truncate(0)
        f.close()
    file = open(path, 'w')
    file.write(msg)
    file.close()
'''
 
'''def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        # print(path + ' successful creat')
        return True'''