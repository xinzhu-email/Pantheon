<<<<<<< HEAD
import os, sys
=======
import os, sys, io, ast, pkgutil, pkg_resources
import subprocess
>>>>>>> extension
from PyQt5 import QtCore, QtGui
# import mysql.connector
from pathlib import Path
from appdirs import AppDirs
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

<<<<<<< HEAD
=======
# create center directory to store all kinds of data
try: 
    version = pkg_resources.get_distribution("scpantheon").version
except:
    subprocess.check_call(['pip3', 'install', "scpantheon"])
    version = pkg_resources.get_distribution("scpantheon").version

import requests, zipfile, tarfile, shutil, subprocess
    
from appdirs import AppDirs
import pkg_resources
global dir
appname = "scpantheon"
appauthor = "xinzhu"
dirs = AppDirs(appname, appauthor, version)
dir = dirs.user_data_dir 

>>>>>>> extension
sys.path.append(str(Path(__file__).resolve().parents[1]))

class Ui_Dialog(QDialog, QWidget, object):
    my_signal = pyqtSignal(str)
<<<<<<< HEAD
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Choose")
        Dialog.resize(750, 600)
=======

    def __init__(self):
        super(Ui_Dialog, self).__init__()
    
    def setupUi(self, Dialog):
        Dialog.setObjectName("Data Panel")
        Dialog.resize(750, 400)
>>>>>>> extension
        self.cwd = os.getcwd()
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setWeight(20)
<<<<<<< HEAD

        # render help text
        self.text_brow = QTextBrowser()

        # Choose path button
        self.btn_Extensions = QPushButton("Browse for Extensions folder",self)  
=======
        # render help text
        self.text_brow = QTextBrowser()

        '''# Choose path button
        self.btn_Extensions = QPushButton("Choose New Extensions folder",self)  
>>>>>>> extension
        self.btn_Extensions.setObjectName("btn_Extensions")  
        self.btn_Extensions.clicked.connect(self.slot_btn_Extensions)
        self.btn_Extensions.setFont(font)
        self.btn_Extensions.setMinimumSize(750, 100)
<<<<<<< HEAD
        # self.btn_Extensions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Choose file button
        self.btn_Data = QPushButton("Browse for Data files",self)  
        self.btn_Data.setObjectName("btn_Data")  
        self.btn_Data.clicked.connect(self.slot_btn_Data)
        self.btn_Data.setFont(font)
        self.btn_Data.setMinimumSize(750, 100)
        # self.btn_Data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Start scpantheon
        self.btn_Start = QPushButton("Load last dataset used",self)
        self.btn_Start.setObjectName("btn_Start")
        self.btn_Start.clicked.connect(lambda : self.Load(Dialog))
=======
        # self.btn_Extensions.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)'''
        # Choose Data File Button
        self.btn_Data_File = QPushButton("Choose New Data File",self)  
        self.btn_Data_File.setObjectName("btn_Data_File")  
        self.btn_Data_File.clicked.connect(self.slot_btn_Data_file)
        self.btn_Data_File.setFont(font)
        self.btn_Data_File.setMinimumSize(750, 100)
        # self.btn_Data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Choose Data Folder Button
        self.btn_Data_Folder = QPushButton("Choose New Data Folder",self)  
        self.btn_Data_Folder.setObjectName("btn_Data_Folder")  
        self.btn_Data_Folder.clicked.connect(self.slot_btn_Data_folder)
        self.btn_Data_Folder.setFont(font)
        self.btn_Data_Folder.setMinimumSize(750, 100)
        # self.btn_Data.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Start scpantheon
        self.btn_Start = QPushButton("Data Not Found",self)
        self.btn_Start.setObjectName("btn_Start")
        self.btn_Start.clicked.connect(lambda : self.Run(Dialog))
>>>>>>> extension
        self.btn_Start.setFont(font)
        self.btn_Start.setMinimumSize(750, 100)
        # self.btn_Start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

<<<<<<< HEAD
        self.layout1 = QVBoxLayout()
        self.layout2 = QVBoxLayout(Dialog)
        self.layout2.setObjectName("Layout2")    
        self.layout2.addWidget(self.text_brow)             
=======
        self.layout = QVBoxLayout(Dialog)
        self.layout.setObjectName("layout")    
        self.layout.addWidget(self.text_brow)             
>>>>>>> extension

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setObjectName("buttonBox")
<<<<<<< HEAD
        self.layout2.addWidget(self.buttonBox)

        self.layout2.addWidget(self.btn_Extensions)
        self.layout2.addWidget(self.btn_Data)
        self.layout2.addWidget(self.btn_Start)
=======
        self.layout.addWidget(self.buttonBox)

        '''self.layout.addWidget(self.btn_Extensions)'''
        self.layout.addWidget(self.btn_Data_File)
        self.layout.addWidget(self.btn_Data_Folder)
        self.layout.addWidget(self.btn_Start)
>>>>>>> extension

        # self.retranslateUi(Dialog) 
        # self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        try:
<<<<<<< HEAD
            extension_path, data_file = openreadtxt(dir)  
            self.text_brow.append('original extensions path:' + extension_path + '\noriginal data path:' + data_file + '\n')
        except:
            print('please choose your files') 

=======
            '''extensions_path, data_file = read_path(dir) '''
            extensions_file, data = read_path(dir) 
            if data != '':
                self.btn_Start.setText("Run Previous Data")
                self.text_brow.setText("\t\t\tPrevious Data Path:\n\t" + data)
            else:
                self.btn_Data_File.setText("Choose A New Data File!")
                self.btn_Data_Folder.setText("Choose A New Data Folder")
                self.text_brow.setText("\t\t\tData Not Found...")
            '''auto_pip_install(extensions_path) '''
        except:
            self.btn_Data_File.setText("Choose A New Data File!")
            self.btn_Data_Folder.setText("Choose A New Data Folder")
            self.text_brow.setText("\t\t\tData Not Found...")
>>>>>>> extension

    def event(self, event):
        if event.type()==QtCore.QEvent.EnterWhatsThisMode:
            QWhatsThis.leaveWhatsThisMode()
<<<<<<< HEAD
            self.text_brow.setText("Choose your extension packages and your data") 
        return QDialog.event(self,event)

    def slot_btn_Extensions(self):
        global Extensions
        Extensions = QFileDialog.getExistingDirectory(self,"Choose Extensions",self.cwd) # 起始路径
        if Extensions == "":
            print("\nchoose canceled")
            return

        # write extension into user_data_dir
        text_create('extension_path', Extensions)
        print("\nExtensions:",Extensions)
        self.text_brow.append("new extensions path:"+Extensions)

    def slot_btn_Data(self):
        global Data
        Data, file_type = QFileDialog.getOpenFileName(self,"Choose Data", self.cwd)   # 设置文件扩展名过滤,用双分号间隔

        if Data == "":
            print("\nchoose canceled")
            return

        # write Data into user_data_dir
        text_create('data_file', Data)
        print("\nData:",Data)
        self.text_brow.append("new data path:"+Data)
        self.btn_Start.setText("Load new dataset")

    def Load(self, Dialog):
        Dialog.reject()
        check_code = 'app closed'
        self.my_signal.emit(check_code)


    '''def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Choose", "Choose"))'''
=======
            # self.text_brow.setText("Choose your extension packages and your data") 
        return QDialog.event(self,event)

    '''def slot_btn_Extensions(self):
        global Extensions
        Extensions = QFileDialog.getExistingDirectory(self," ",self.cwd) # 起始路径
        # write extension into user_data_dir
        if Extensions != '':
           write_msg('extensions_path', Extensions)'''

    def slot_btn_Data_file(self):
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
    
    def slot_btn_Data_folder(self):
        global Data
        Data = QFileDialog.getExistingDirectory(self, " ", self.cwd)   # 设置文件扩展名过滤,用双分号间隔
        if Data == "":
            # print("\nchoose canceled")
            return
        # write Data into user_data_dir
        write_msg('data_file', Data)
        # print("Data:",Data)
        # self.text_brow.append("new data path:"+Data)
        self.btn_Start.setText("Run New Data!")
        self.text_brow.setText("\t\t\tNew Data Folder Path:\n\t" + Data)

    def Run(self, Dialog):
        global check_code
        check_code = 'app closed'
        Dialog.reject() 

# extract online extension zip
def extract_online_packages(extensions_path, extract_path, url='https://github.com/xinzhu-email/Pantheon/archive/refs/heads/main.zip'):
    r = requests.get(url, stream=True) 
    try:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall(extract_path)
        print("get zip file")
    except zipfile.BadZipFile:
        try:
            t = tarfile.open(fileobj=io.BytesIO(r.content), mode="r:gz")  
            t.extractall(extract_path)
            print("get tar file")
        except tarfile.ReadError:
            print("zip or tar file is needed")
    
    # Find all the directory from new local extension that has module.py
    module_path_list = []
    def find_module(path):
        lsdir = os.listdir(path)
        dirs = [i for i in lsdir if os.path.isdir(os.path.join(path, i))]
        if dirs:
            for i in dirs:
                find_module(os.path.join(path, i))
        files = [i for i in lsdir if os.path.isfile(os.path.join(path,i))]
        flag = False
        for f in files:
            if f == 'module.py':
                flag = True
                # module_path_list.append(os.path.join(path, f))
        if flag: 
            module_path_list.append(path)

    find_module(extract_path)
    print('module path list:\n', module_path_list)
    # Copy all the extension module to extension path
    for module_directory in module_path_list:
        module_directory += '/'
        folder_name = os.path.basename(module_directory[:-1])
        try: 
            shutil.copytree(module_directory, extensions_path+'/'+folder_name+'/')
            print('Module', folder_name, 'added')
        except:
            print('Module', folder_name, 'already exists')
    print('Online packages download finished!')
    auto_pip_install(extensions_path)

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
>>>>>>> extension


def mkdir(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
<<<<<<< HEAD
        print(path + ' successful creat')
        return True
    else:
        print(path + ' already exist')


def text_create(name, msg):
    path = dir + "/" + name + '.txt'
    print("-========- path:", path)
=======
        # print('current version:' + path + ' successful creat')
        return True

def write_msg(name, msg):
    path = dir + "/" + name + '.txt'
    # print("-========- path:", path)
>>>>>>> extension
    with open(path, "w") as f:
        f.truncate(0)
        f.close()
    file = open(path, 'w')
    file.write(msg)
    file.close()

<<<<<<< HEAD

def openreadtxt(dir):
    e_file = open(dir + '/' + 'extension_path.txt', 'r')
    e_path = e_file.readline()
    e_file.close()
    print('-======- e_path:', e_path)
    d_file = open(dir + '/' + 'data_file.txt', 'r')
    data = d_file.readline()
    print('-======- data:', data)
    d_file.close()
    return e_path, data

=======
def read_path(dir):
    try:
        e_file = open(dir + '/' + 'extensions_path.txt', 'r')
        new_extensions_path = e_file.readline()
        if(new_extensions_path == ''):
            new_extensions_path = dir + '/extensions'
            new_extract_path = dir + '/online_extract'
            if not os.path.exists(new_extensions_path):
                os.makedirs(new_extensions_path)
            if not os.path.exists(new_extract_path):
                os.makedirs(new_extract_path)
            write_msg('extensions_path', new_extensions_path)
            extract_online_packages(new_extensions_path, new_extract_path)
        e_file.close()
        # print('-======- e_path:', new_extensions_path)
    except:
        # self create extensions path and automatically download Default patheon extensions
        new_extensions_path = dir + '/extensions'
        new_extract_path = dir + '/online_extract'
        if not os.path.exists(new_extensions_path):
            os.makedirs(new_extensions_path)
        if not os.path.exists(new_extract_path):
            os.makedirs(new_extract_path)
        write_msg('extensions_path', new_extensions_path)
        extract_online_packages(new_extensions_path, new_extract_path)

    try:
        d_file = open(dir + '/' + 'data_file.txt', 'r')
    except:
        new_extensions_path = dir + '/extensions'
        if not os.path.exists(new_extensions_path):
            os.makedirs(new_extensions_path)
            
    data = d_file.readline()
    # print('-======- data:', data)
    d_file.close()
    return new_extensions_path, data
>>>>>>> extension

def signal_slot(data):
    global check_code
    # print("check code:", data)
    check_code = data


def main():
<<<<<<< HEAD
    global dir
    # create the file to write data
    appname = "scpantheon"
    appauthor = "xinzhu"
    version = "0.2.1"
    dirs = AppDirs(appname, appauthor, version)
    dir = dirs.user_data_dir
=======
    global check_code, dir
    check_code = "app_running"
    print("center directory path:\n\t", dir)
>>>>>>> extension
    mkdir(path=dir)
    # create qt app
    app = QApplication(sys.argv)
    Dialog = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
<<<<<<< HEAD
    ui.my_signal.connect(signal_slot)
    Dialog.show()
    app.exec()
    try: return check_code
    except: return 'app ended'

# 利用'app closed' 使 X 是关闭
=======
    Dialog.setWindowFlags(Dialog.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)  
    Dialog.show()
    Dialog.setWindowFlags(Dialog.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint) 
    Dialog.show()
    app.exec()
    return check_code
>>>>>>> extension
