import os
import shutil

path = 'C:/Users/23606/Documents/Workspace/Pantheon/online_extension_packages/'

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

find_module(path=path)
print('module path list:\n', module_path_list)
	
for module_directory in module_path_list:
    module_directory += '/'
    folder_name = os.path.basename(module_directory[:-1])
    try: 
        shutil.copytree(module_directory, 'C:/Users/23606/Documents/Workspace/Pantheon/online_extension_packages/zzz/'+folder_name+'/')
    except:
        print('Module', folder_name, 'already exists')