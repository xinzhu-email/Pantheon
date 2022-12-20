import os, sys
import importlib
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSlot
from bokeh.events import ButtonClick
from PyQt5 import QtCore, QtGui, QtWidgets,QtWebEngineWidgets
import mysql.connector

def myconnect():
    global mydb,mycursor
    mydb = mysql.connector.connect(
        host="localhost",
        #  port=3360,
        user="root",
        password="1122cccc",
        database = "mybase"
    )
    mycursor = mydb.cursor()


def creatbase():
    global mycursor, mydb
    mycursor.execute("CREATE DATABASE mybase")
    mydb.database = "mybase"

def creatable():
    global mycursor,mydb
    mycursor.execute("CREATE TABLE vlist (value VARCHAR(255))")
    mydb.commit()

def insert(path): # str -> tuple
    global mydb,mycursor
    insert = "INSERT INTO vlist (value) VALUES (%s)"
    thistuple = (path,)
    print(thistuple)
    mycursor.execute(insert, thistuple)
    mydb.commit()
    

class Ui_Dialog(QWidget, object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(3000,1500)
        self.cwd = os.getcwd()

        # choose path button
        self.btn_chooseDir = QPushButton("choose a dir", self)  
        self.btn_chooseDir.setObjectName("btn_chooseDir")  
        self.btn_chooseDir.clicked.connect(self.slot_btn_chooseDir)


        # choose file button
        self.btn_chooseFile = QPushButton("choose a file", self)  
        self.btn_chooseFile.setObjectName("btn_chooseFile")  
        self.btn_chooseFile.clicked.connect(self.slot_btn_chooseFile)

        
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.btn_chooseDir)
        self.layout1.addWidget(self.btn_chooseFile)
        self.layout2 = QVBoxLayout(Dialog)
        self.layout2.setObjectName("Layout2")


        # render website inside qt application
        self.centralwidget = QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.webEngineView = QWebEngineView(self.centralwidget)
        self.webEngineView.load(QtCore.QUrl.fromLocalFile("/D:/anaconda/Lib/site-packages/scpantheon/embed.html"))
        self.layout2.addWidget(self.webEngineView)


        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.layout2.addWidget(self.buttonBox)

        self.layout2.addWidget(self.btn_chooseDir)
        self.layout2.addWidget(self.btn_chooseFile)


        self.retranslateUi(Dialog) 
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def slot_btn_chooseDir(self):
        # global path_

        dir_choose = QFileDialog.getExistingDirectory(self,"choose dir",self.cwd) # 起始路径
        if dir_choose == "":
            print("\nchoose canceled")
            return

        insert(dir_choose)
        print("\npath_:",dir_choose)

    def slot_btn_chooseFile(self):
        # global file_name

        fileName_choose, file_type = QFileDialog.getOpenFileName(self,"Choose file", self.cwd)   # 设置文件扩展名过滤,用双分号间隔

        if fileName_choose == "":
            print("\nchoose canceled")
            return

        insert(fileName_choose)
        print("\nfile_name:",fileName_choose)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))


def main():
    # Create mysql database
    try: myconnect()
    except:
        try: creatbase()
        except: 
            '''delete = "DROP TABLE IF EXISTS vlist"
            mycursor.execute(delete)'''
    try:creatable() # vlist is the table name
    except: ()
    # create qt app
    app = QApplication(sys.argv)
    '''settings = QtWebEngineWidgets.QWebEngineSettings.defaultSettings()
    settings.setAttribute(QtWebEngineWidgets.QWebEngineSettings.LocalContentCanAccessRemoteUrls, True)'''
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

# main()

'''

name 传不进去
mysql语法太死了

'''

'''

filename = os.path.split(file_name)[1]
filetype = os.path.splitext(filename)[-1][1:]
if filetype == 'csv':

'''