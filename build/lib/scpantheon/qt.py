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
        Dialog.setObjectName("ScPantheon")
        Dialog.resize(2000,1200)
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)

        # choose path button
        self.btn_Extensions = QPushButton("Extensions", self)  
        self.btn_Extensions.setObjectName("btn_Extensions")  
        self.btn_Extensions.clicked.connect(self.slot_btn_Extensions)
        self.btn_Extensions.setFont(font)
        self.btn_Extensions.setFixedWidth(400)

        # choose file button
        self.btn_Data = QPushButton("Data", self)  
        self.btn_Data.setObjectName("btn_Data")  
        self.btn_Data.clicked.connect(self.slot_btn_Data)
        self.btn_Data.setFont(font)
        self.btn_Data.setFixedWidth(400)
        
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.btn_Extensions)
        self.layout1.addWidget(self.btn_Data)
        self.layout2 = QVBoxLayout(Dialog)
        self.layout2.setObjectName("Layout2")


        # render website inside qt application
        self.centralwidget = QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.webEngineView = QWebEngineView(self.centralwidget)
        self.webEngineView.load(QtCore.QUrl.fromLocalFile("D:/anaconda/Lib/site-packages/Pantheon/scpantheon/embed.html"))
        self.layout2.addWidget(self.webEngineView)


        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.layout2.addWidget(self.buttonBox)

        self.layout2.addWidget(self.btn_Extensions)
        self.layout2.addWidget(self.btn_Data)


        self.retranslateUi(Dialog) 
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def slot_btn_Extensions(self):
        Extensions = QFileDialog.getExistingDirectory(self,"Choose Extensions",self.cwd) # 起始路径
        if Extensions == "":
            print("\nchoose canceled")
            return

        insert(Extensions)
        print("\nExtensions:",Extensions)

    def slot_btn_Data(self):
        Data, file_type = QFileDialog.getOpenFileName(self,"Choose Data", self.cwd)   # 设置文件扩展名过滤,用双分号间隔

        if Data == "":
            print("\nchoose canceled")
            return

        insert(Data)
        print("\nData:",Data)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("ScPantheon", "ScPantheon"))


def main():
    # Create mysql database
    try: myconnect()
    except: creatbase()
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
    app.exec()
    return 'app closed'
