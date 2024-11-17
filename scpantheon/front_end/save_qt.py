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
        Dialog.setObjectName("Local Data Storer")
        Dialog.resize(750,300)
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)

        # render help text
        self.text_brow = QTextBrowser()

        # choose path button
        self.btn_save = QPushButton("Choose New Saving Path", self)  
        self.btn_save.setObjectName("btn_save")  
        self.btn_save.clicked.connect(self.slot_btn_save)
        self.btn_save.setFont(font)
        self.btn_save.setMinimumSize(750, 100)

        # Start load
        self.btn_Start = QPushButton("Saving Path Not Found",self)
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

        self.layout.addWidget(self.btn_save)
        self.layout.addWidget(self.btn_Start)

        # self.retranslateUi(Dialog) 
        # self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        try:
            save_path = get_save_path(dir)
            if save_path != '':
                self.btn_Start.setText("Save Data In The Previous Path")
                self.text_brow.setText("\t\t\tPrevious Saving Path:\n\t" + save_path)
            else:
                self.btn_save.setText("Choose A Saving Path!")
                self.text_brow.setText("\t\t\tSaving Path Not Found...")
        except:
            self.btn_save.setText("Choose A Saving Path!")
            self.text_brow.setText("\t\t\tSaving Path Not Found...")

    def event(self, event):
        if event.type()==QtCore.QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            self.text_brow.setText("Choose the path you want to save your file")
        return QDialog.event(self,event)

    def slot_btn_save(self):
        save = QFileDialog.getExistingDirectory(self,"Choose save",self.cwd) # 起始路径
        # write extension into user_data_dir
        if save != '':
            write_msg('save_path', save)
        self.btn_Start.setText("Save Data In The New Path!")
        self.text_brow.setText("\t\t\tNew Saving Path:\n\t" + save)

    def Load(self, Dialog):
        global check_code
        check_code = 'app closed'
        Dialog.reject()
        # self.my_signal.emit(check_code)

def get_save_path(dir):
    s_file = open(dir + '/' + 'save_path.txt', 'r')
    s_path = s_file.readline()
    s_file.close()
    # print('-======- s_path', s_path)
    return s_path

def main():
    global check_code
    check_code = "app_running"
    mkdir(path=dir)
    # create qt app
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    # Dialog.show()
    # bring window to top and act like a "normal" window!
    Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  # set always on top flag, makes window disappear
    Dialog.show() # makes window reappear, but it's ALWAYS on top
    '''Dialog.setWindowFlags(Dialog.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint) # clear always on top flag, makes window disappear
    Dialog.show()  # makes window reappear, acts like normal window now (on top now but can be underneath if you raise another window)'''
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
    file.close()'''
 
'''def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        # print(path + ' successful creat')
        return True'''