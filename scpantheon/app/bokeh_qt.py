import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QUrl, QStandardPaths
# import mysql.connector
from pathlib import Path
from appdirs import AppDirs
from PyQt5.QtNetwork import QNetworkCookieJar
import pkg_resources, subprocess

try:
    version = pkg_resources.get_distribution("scpantheon").version
except pkg_resources.DistributionNotFound:
    subprocess.check_call(['pip3', 'install', "scpantheon"])
    version = pkg_resources.get_distribution("scpantheon").version

sys.path.append(str(Path(__file__).resolve().parents[1]))

class Ui_Dialog(QWidget, object):
    def __init__(self):
        super(Ui_Dialog, self).__init__()

    def setupUi(self, Dialog):
        # default setting
        Dialog.setObjectName("ScPantheon")
        Dialog.resize(1500,960)
        # self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowStaysOnBottomHint)
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)

        # create layout
        self.layout = QVBoxLayout(Dialog)
        self.layout.setObjectName("layout")

        # render website inside qt application
        self.centralwidget = QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.webEngineView = QWebEngineView(self.centralwidget)
        url = "http://localhost:5006/"
        self.webEngineView.load(QUrl(url))
        self.layout.addWidget(self.webEngineView)
        print("webengine widget added!")

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.layout.addWidget(self.buttonBox)

        # self.retranslateUi(Dialog) 
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    # def loadPage(self):
    #     print("Load Page!")
    #     self.webEngineView.load(QUrl("http://baidu.com"))
    #     print("Load Page!")
    #     '''Func = open("embed.html","w")
    #     Func.write("<!doctype html>\n<html>\n<iframe src='http://localhost:5006/'\nname='thumbnails'\nframeborder='0'\nstyle='width: 100%; height: 1500px;'>\n</html>")
    #     Func.close()
    #     with open('embed.html', 'r') as f:
    #         html = f.read()
    #         self.webEngineView.setHtml(html)'''

    # '''def retranslateUi(self, Dialog):
    #     _translate = QtCore.QCoreApplication.translate
    #     Dialog.setWindowTitle(_translate("ScPantheon", "ScPantheon"))'''


def main():
    global check_code
    check_code = "app closed"
    # create qt app
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec()
    return check_code
