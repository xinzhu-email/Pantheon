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
    def setupUi(self, Dialog):
        Dialog.setObjectName("Choose")
        Dialog.resize(750,300)
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)

        # render help text
        self.text_brow = QTextBrowser()

        # choose path button
        self.btn_save = QPushButton("output", self)  
        self.btn_save.setObjectName("btn_save")  
        self.btn_save.clicked.connect(self.slot_btn_save)
        self.btn_save.setFont(font)
        self.btn_save.setMinimumSize(750, 100)
        
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.btn_save)
        self.layout2 = QVBoxLayout(Dialog)
        self.layout2.setObjectName("Layout2")    
        self.layout2.addWidget(self.text_brow)             

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setObjectName("buttonBox")
        self.layout2.addWidget(self.buttonBox)

        self.layout2.addWidget(self.btn_save)

        # self.retranslateUi(Dialog) 
        # self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        output_path = self.get_save_path() + '\\'
        self.text_brow.append('original output path:' + output_path)


    def event(self, event):
        if event.type()==QtCore.QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            self.text_brow.setText("Choose the path you want to save your file")
        return QDialog.event(self,event)

    def slot_btn_save(self):
        save = QFileDialog.getExistingDirectory(self,"Choose save",self.cwd) # 起始路径
        if save == "":
            print("\nchoose canceled")
            return

        # write extension into user_data_dir
        text_create('save_path', save)
        print("\nsave:", save) 
        self.text_brow.append("new output path:" + save)

    def get_save_path(self):
        s_file = open(dir + '/' + 'save_path.txt', 'r')
        s_path = s_file.readline()
        s_file.close()
        print('-======- s_path', s_path)
        return s_path

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
    path = dir + "\\" + name + '.txt'
    print("-========- path:", path)
    with open(path, "w") as f:
        f.truncate(0)
        f.close()
    file = open(path, 'w')
    file.write(msg)
    file.close()


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
    Dialog.show()
    app.exec()
    return 'app closed'

