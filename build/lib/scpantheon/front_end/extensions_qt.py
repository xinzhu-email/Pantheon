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

    def setupUi(self, Dialog):
        Dialog.setObjectName("Local Packages Loader")
        Dialog.resize(750,300)
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)

        # render help text
        self.text_brow = QTextBrowser()

        # choose path button
        self.btn_extensions = QPushButton("Choose New Extensions Path", self)  
        self.btn_extensions.setObjectName("btn_extensions")  
        self.btn_extensions.clicked.connect(self.slot_btn_extensions)
        self.btn_extensions.setFont(font)
        self.btn_extensions.setMinimumSize(750, 100)

        # Start load
        self.btn_Start = QPushButton("Extensions Path Not Found",self)
        self.btn_Start.setObjectName("btn_Start")
        self.btn_Start.clicked.connect(lambda : self.Load(Dialog))
        self.btn_Start.setFont(font)
        self.btn_Start.setMinimumSize(750, 100)
        
        self.layout = QVBoxLayout(Dialog)
        self.layout.setObjectName("layout")    
        self.layout.addWidget(self.text_brow)             

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setObjectName("buttonBox")
        self.layout.addWidget(self.buttonBox)

        self.layout.addWidget(self.btn_extensions)
        self.layout.addWidget(self.btn_Start)

        # self.retranslateUi(Dialog) 
        # self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        try:
            extensions_path = get_extensions_path(dir)
            if extensions_path != '':
                self.btn_Start.setText("Load Previous Extensions")
                self.text_brow.setText("\t\t\tPrevious Extensions Path:\n\t" + extensions_path)
            else:
                self.btn_extensions.setText("Choose New Extensions Path!")
                self.text_brow.setText("\t\t\tExtensions Path Not Found...")
        except:
            self.btn_extensions.setText("Choose New Extensions Path!")
            self.text_brow.setText("\t\t\tExtensions Path Not Found...")

    def event(self, event):
        if event.type()==QtCore.QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            self.text_brow.setText("Choose New Extensions Path")
        return QDialog.event(self,event)

    def slot_btn_extensions(self):
        extensions = QFileDialog.getExistingDirectory(self,"Choose extensions",self.cwd) # 起始路径
        # write extension into user_data_dir
        if extensions != '':
            write_msg('extensions_path', extensions)
        self.btn_Start.setText("Load New Extensions!")
        self.text_brow.setText("\t\t\tNew Extensions Path:\n\t" + extensions)

    def Load(self, Dialog):
        global check_code
        check_code = 'app closed'
        Dialog.reject()
        # self.my_signal.emit(check_code)

def get_extensions_path(dir):
    e_file = open(dir + '/' + 'extensions_path.txt', 'r')
    e_path = e_file.readline()
    e_file.close()
    return e_path 


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
    Dialog.setWindowFlags(Dialog.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint) 
    Dialog.show()
    app.exec()
    return check_code