import os, sys, io, ast, pkgutil, pkg_resources
import subprocess
import re
import hashlib
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
        self.btn_Start.setFont(font)
        self.btn_Start.setMinimumSize(750, 100)
        # self.btn_Start.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.layout = QVBoxLayout(Dialog)
        self.layout.setObjectName("layout")    
        self.layout.addWidget(self.text_brow)             

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setObjectName("buttonBox")
        self.layout.addWidget(self.buttonBox)

        '''self.layout.addWidget(self.btn_Extensions)'''
        self.layout.addWidget(self.btn_Data_File)
        self.layout.addWidget(self.btn_Data_Folder)
        self.layout.addWidget(self.btn_Start)

        # self.retranslateUi(Dialog) 
        # self.buttonBox.accepted.connect(self.accepted)
        self.buttonBox.rejected.connect(self.rejected)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        try:
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
def extract_online_packages(extract_path, url: str | None ='https://github.com/xinzhu-email/Pantheon/archive/refs/heads/Extension.zip'):
    print("extract_path:", extract_path)
    r = requests.get(url, stream=True) 

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
        if flag: 
            module_path_list.append(path)
    find_module(extract_path)

    def get_md5(file_path):
        md5 = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                md5.update(data)
        return md5.hexdigest()
    
    max_versions = {}
    pattern = re.compile(r'_(\d+)$')
    for folder in module_path_list:
        match = pattern.search(folder)
        if match:
            version = int(match.group(1))
            prefix = os.path.basename(folder.rsplit('_', 1)[0])
            if prefix not in max_versions or version > max_versions[prefix]:
                max_versions[prefix] = version
        elif os.path.basename(folder) not in max_versions:
            prefix = os.path.basename(folder)
            max_versions[prefix] = 0    
    
    def extract_module(target_file):
        rel_target = os.path.dirname(os.path.dirname(target_file))
        relative_path = os.path.relpath(target_file, rel_target)
        module_name = os.path.dirname(relative_path)
        if module_name not in max_versions.keys():
            final_path = os.path.join(extract_path, module_name)
            file_pwd = os.path.join(final_path, 'module.py')
            with z.open(target_file) as file_in_zip:
                if not os.path.exists(final_path):
                    os.mkdir(final_path)
                    with open(file_pwd, 'wb') as file_out:
                        file_out.write(file_in_zip.read())
        else:
            module_name_version = module_name + '_' + str(max_versions[module_name] + 1)
            final_path = os.path.join(extract_path, module_name_version)
            file_pwd = os.path.join(final_path, 'module.py')
            with z.open(target_file) as file_in_zip:
                if not os.path.exists(final_path):
                    os.mkdir(final_path)
                    with open(file_pwd, 'wb') as file_out:
                        file_out.write(file_in_zip.read())
            hash_new = get_md5(file_pwd)
            pattern = re.compile(r'_(\d+)$')
            for folder in module_path_list:
                match = pattern.search(folder)
                if match:
                    version = int(match.group(1))
                    prefix = os.path.basename(folder.rsplit('_', 1)[0])
                    if prefix == module_name and version != max_versions[module_name] + 1:
                        hash_local = get_md5(os.path.join(folder, 'module.py'))
                        print("repeated local hash", hash_local, hash_new)
                        if hash_local == hash_new:
                            shutil.rmtree(final_path)
                            print("New extension", module_name, "is the same as", os.path.basename(folder))
                            return                    
                elif max_versions[module_name] == 0 and os.path.basename(folder) == module_name:
                    hash_local = get_md5(os.path.join(folder, 'module.py'))
                    if hash_local == hash_new:
                        shutil.rmtree(final_path)
                        print("New extension", module_name, "is the same as", module_name)
                        return            

    try:
        z = zipfile.ZipFile(io.BytesIO(r.content))
        print("get zip file")
        z_files = z.namelist()
        z_modules = [name for name in z_files if name.endswith('module.py')]
        for target_file in z_modules:
            extract_module(target_file)
        
    except zipfile.BadZipFile:
        try:
            t = tarfile.open(fileobj=io.BytesIO(r.content), mode="r:gz")  
            print("get tar file")
            t_files = t.getnames()
            t_modules = [name for name in t_files if name.endswith('module.py')]
            for target_file in t_modules:
                extract_module(target_file)
        except tarfile.ReadError:
            print("zip or tar file is needed")

    module_path_list = []
    find_module(module_path_list)
    print("Extensions list updated with modules:")
    for module_directory in module_path_list:
        module_directory += '/'
        folder_name = os.path.basename(module_directory[:-1])
        print(folder_name)
    print('Online packages download finished!')
    auto_pip_install(extract_path)

# fetch every module from each module.py in extension folder
def auto_pip_install(folder_path):
    try:
        all_imports = {'import': set(), 'from': set()}
        for root, files in os.walk(folder_path):
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
        new_extensions_path = e_file.readline()
        if(new_extensions_path == ''):
            new_extensions_path = dir + '/extensions'
            if not os.path.exists(new_extensions_path):
                os.makedirs(new_extensions_path)
            write_msg('extensions_path', new_extensions_path)
            extract_online_packages(new_extensions_path)
        e_file.close()
        # print('-======- e_path:', new_extensions_path)
    except:
        # self create extensions path and automatically download Default patheon extensions
        new_extensions_path = dir + '/extensions'
        if not os.path.exists(new_extensions_path):
            os.makedirs(new_extensions_path)
        write_msg('extensions_path', new_extensions_path)
        extract_online_packages(new_extensions_path)

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
