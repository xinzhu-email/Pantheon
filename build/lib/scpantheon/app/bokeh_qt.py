import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QUrl, QStandardPaths
# import mysql.connector
from pathlib import Path
from appdirs import AppDirs
from PyQt5.QtNetwork import QNetworkCookieJar
<<<<<<< HEAD
=======
import pkg_resources, subprocess

try:
    version = pkg_resources.get_distribution("scpantheon").version
except pkg_resources.DistributionNotFound:
    subprocess.check_call(['pip', 'install', "scpantheon"])
    version = pkg_resources.get_distribution("scpantheon").version
>>>>>>> extension

sys.path.append(str(Path(__file__).resolve().parents[1]))

class Ui_Dialog(QWidget, object):
<<<<<<< HEAD
    def setupUi(self, Dialog):
        Dialog.setObjectName("ScPantheon")
        Dialog.resize(1600,1000)
        Dialog.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
=======
    def __init__(self):
        super(Ui_Dialog, self).__init__()

    def setupUi(self, Dialog):
        # default setting
        Dialog.setObjectName("ScPantheon")
        Dialog.resize(1500,960)
        # self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowStaysOnBottomHint)
>>>>>>> extension
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)

<<<<<<< HEAD
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout(Dialog)
        self.layout2.setObjectName("Layout2")
=======
        # create layout
        self.layout = QVBoxLayout(Dialog)
        self.layout.setObjectName("layout")
>>>>>>> extension

        # render website inside qt application
        self.centralwidget = QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.webEngineView = QWebEngineView(self.centralwidget)
        url = "http://localhost:5006/"
        self.webEngineView.load(QUrl(url))
<<<<<<< HEAD
        print("url opened")
        self.layout2.addWidget(self.webEngineView)
=======
        self.layout.addWidget(self.webEngineView)
>>>>>>> extension


        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
<<<<<<< HEAD
        self.layout2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog) 
=======
        self.layout.addWidget(self.buttonBox)

        # self.retranslateUi(Dialog) 
>>>>>>> extension
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def loadPage(self):
        # self.webEngineView.load(QUrl("http://baidu.com"))
        Func = open("embed.html","w")
<<<<<<< HEAD
        # 编写html
=======
>>>>>>> extension
        Func.write("<!doctype html>\n<html>\n<iframe src='http://localhost:5006/'\nname='thumbnails'\nframeborder='0'\nstyle='width: 100%; height: 2000px;'>\n</html>")
        Func.close()
        with open('embed.html', 'r') as f:
            html = f.read()
            self.webEngineView.setHtml(html)

<<<<<<< HEAD
    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("ScPantheon", "ScPantheon"))


def main():
    global dir
=======
    '''def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("ScPantheon", "ScPantheon"))'''


def main():
    global check_code
    check_code = "app closed"
>>>>>>> extension
    # create qt app
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec()
<<<<<<< HEAD
    return 'app closed'
=======
    return check_code
>>>>>>> extension
