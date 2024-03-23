import os, sys
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QUrl, QStandardPaths
# import mysql.connector
from pathlib import Path
from appdirs import AppDirs
from PyQt5.QtNetwork import QNetworkCookieJar

sys.path.append(str(Path(__file__).resolve().parents[1]))

class Ui_Dialog(QWidget, object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("ScPantheon")
        Dialog.resize(1600,1000)
        Dialog.setWindowFlags(QtCore.Qt.WindowMinMaxButtonsHint | QtCore.Qt.WindowCloseButtonHint)
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)

        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout(Dialog)
        self.layout2.setObjectName("Layout2")

        # render website inside qt application
        self.centralwidget = QWidget(Dialog)
        self.centralwidget.setObjectName("centralwidget")
        self.webEngineView = QWebEngineView(self.centralwidget)
        self.loadPage()
        self.layout2.addWidget(self.webEngineView)


        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.layout2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog) 
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def loadPage(self):
        # self.webEngineView.load(QUrl("http://baidu.com"))
        Func = open("embed.html","w")
        # 编写html
        Func.write("<!doctype html>\n<html>\n<iframe src='http://localhost:5006/'\nname='thumbnails'\nframeborder='0'\nstyle='width: 100%; height: 2000px;'>\n</html>")
        Func.close()
        with open('embed.html', 'r') as f:
            html = f.read()
            self.webEngineView.setHtml(html)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("ScPantheon", "ScPantheon"))


def main():
    global dir
    # create qt app
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    app.exec()
    return 'app closed'
