import os, sys, ast, pkgutil, pkg_resources
import subprocess
from PyQt5 import QtCore, QtGui
# import mysql.connector
from pathlib import Path
from appdirs import AppDirs
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# create center directory to store all kinds of data
try: 
    version = pkg_resources.get_distribution("scpantheon").version
except:
    subprocess.check_call(['pip', 'install', "scpantheon"])
    version = pkg_resources.get_distribution("scpantheon").version
    
from appdirs import AppDirs
import pkg_resources
global dir
appname = "scpantheon"
appauthor = "xinzhu"
dirs = AppDirs(appname, appauthor, version)
dir = dirs.user_data_dir 

sys.path.append(str(Path(__file__).resolve().parents[1]))

class Ui_Dialog(QDialog, QWidget, object):
    my_signal = pyqtSignal(str)

    def __init__(self):
        super(Ui_Dialog, self).__init__()
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Data Panel")
        Dialog.resize(750, 400)
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)
        # render help text
        self.text_brow = QTextBrowser()

        '''# Choose path button
        self.btn_Extensions = QPushButton("Choose New Extensions folder",self)  
        self.btn_Extensions.setObjectName("btn_Extensions")  
        self.btn_Extensions.clicked.connect(self.slot_btn_Extensions)
        self.btn_Extensions.setFont(font)
        self.btn_Extensions.setMinimumSize(750, 100)
        # self.btn_Extensions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)'''
        # Choose file button
        self.btn_Data = QPushButton("Choose New Data File",self)  
        self.btn_Data.setObjectName("btn_Data")  
        self.btn_Data.clicked.connect(self.slot_btn_Data)
        self.btn_Data.setFont(font)
        self.btn_Data.setMinimumSize(750, 150)
        # self.btn_Data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Start scpantheon
        self.btn_Start = QPushButton("Data Not Found",self)
        self.btn_Start.setObjectName("btn_Start")
        self.btn_Start.clicked.connect(lambda : self.Run(Dialog))
        self.btn_Start.setFont(font)
        self.btn_Start.setMinimumSize(750, 150)
        # self.btn_Start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QVBoxLayout(Dialog)
        self.layout.setObjectName("layout")    
        self.layout.addWidget(self.text_brow)             

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setObjectName("buttonBox")
        self.layout.addWidget(self.buttonBox)

        '''self.layout.addWidget(self.btn_Extensions)'''
        self.layout.addWidget(self.btn_Data)
        self.layout.addWidget(self.btn_Start)

        # self.retranslateUi(Dialog) 
        # self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        try:
            '''extensions_path, data_file = read_path(dir) '''
            extensions_file, data_file = read_path(dir) 
            if data_file != '':
                self.btn_Start.setText("Run Previous Data")
                self.text_brow.setText("\t\t\tPrevious Data File Path:\n\t" + data_file)
            else:
                self.btn_Data.setText("Choose A Data File!")
                self.text_brow.setText("\t\t\tData File Not Found...")
            '''auto_pip_install(extensions_path) '''
        except:
            self.btn_Data.setText("Choose A Data File!")
            self.text_brow.setText("\t\t\tData File Not Found...")

    def event(self, event):
        if event.type()==QtCore.QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
            # self.text_brow.setText("Choose your extension packages and your data") 
        return QDialog.event(self,event)

    '''def slot_btn_Extensions(self):
        global Extensions
        Extensions = QFileDialog.getExistingDirectory(self," ",self.cwd) # 起始路径
        # write extension into user_data_dir
        if Extensions != '':
           write_msg('extensions_path', Extensions)'''

    def slot_btn_Data(self):
        global Data
        Data, file_type = QFileDialog.getOpenFileName(self, " ", self.cwd)   # 设置文件扩展名过滤,用双分号间隔
        if Data == "":
            # print("\nchoose canceled")
            return
        # write Data into user_data_dir
        write_msg('data_file', Data)
        # print("Data:",Data)
        # self.text_brow.append("new data path:"+Data)
        self.btn_Start.setText("Run New Data!")
        self.text_brow.setText("\t\t\tNew Data File Path:\n\t" + Data)

    def Run(self, Dialog):
        global check_code
        check_code = 'app closed'
        Dialog.reject() 


# fetch every module from each module.py in extension folder
def auto_pip_install(folder_path):
    try:
        all_imports = {'import': set(), 'from': set()}
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                if file_name == 'module.py':
                    file_path = os.path.join(root, file_name)
                    imports = extract_imports(file_path)
                    all_imports['import'].update(imports['import'])
                    all_imports['from'].update(imports['from'])
    except:
        return
    filtered_imports = {
        'import': filter_standard_libraries(all_imports['import']),
        'from': filter_standard_libraries(all_imports['from'])
    }
    with open('module_requirement.txt', 'w') as req_file:
        required_modules = []
        for imp in filtered_imports['import']:
            req_file.write(f"{imp}\n")
            required_modules.append(imp)
        for frm in filtered_imports['from']:
            req_file.write(f"{frm}\n")
            required_modules.append(frm)
    # use subprocess to pip install required packages
    for module in required_modules:
        print(module)
        try:
            subprocess.check_call(['pip', 'install', module])
            print(f'Succeed to install {module}')
        except subprocess.CalledProcessError as e:
            print(f'Failed to install {module}. Error: {e}')
# fetch every import module from module.py
def extract_imports(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        tree = ast.parse(file.read(), filename=file_path)
    imports = {'import': set(), 'from': set()}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports['import'].add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            imports['from'].add(node.module.split('.')[0])
    return imports
# erase the python sys module 
def filter_standard_libraries(import_set):
    installed_modules = list(set(sys.modules) | {module_info.name.split('.')[0] for module_info in pkgutil.iter_modules()})
    installed_modules.append('rpy2')
    return {lib for lib in import_set if lib not in (installed_modules)}


def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        # print('current version:' + path + ' successful creat')
        return True

def write_msg(name, msg):
    path = dir + "/" + name + '.txt'
    # print("-========- path:", path)
    with open(path, "w") as f:
        f.truncate(0)
        f.close()
    file = open(path, 'w')
    file.write(msg)
    file.close()

def read_path(dir):
    try:
        e_file = open(dir + '/' + 'extensions_path.txt', 'r')
        e_path = e_file.readline()
        e_file.close()
    except:
        # !!! self create extensions path 
        Extensions = ""
        write_msg('extensions_path', Extensions)
        print('Empty Extension Path Created')
        e_file = open(dir + '/' + 'extensions_path.txt', 'r')
        e_path = e_file.readline()
        e_file.close()

    # print('-======- e_path:', e_path)
    d_file = open(dir + '/' + 'data_file.txt', 'r')
    data = d_file.readline()
    # print('-======- data:', data)
    d_file.close()
    return e_path, data

def signal_slot(data):
    global check_code
    # print("check code:", data)
    check_code = data


def main():
    global check_code, dir
    check_code = "app_running"
    print("center directory path:\n\t", dir)
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
