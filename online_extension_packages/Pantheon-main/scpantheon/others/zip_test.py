import requests, zipfile, io, os


zip_file_url = 'https://github.com/xinzhu-email/Pantheon/archive/refs/heads/main.zip'
r = requests.get(zip_file_url, stream=True)
z = zipfile.ZipFile(io.BytesIO(r.content))
z.extractall('C:/Users/23606/Documents/Workspace/Pantheon/output')

# 获取解压后的文件名列表
file_names = z.namelist()

extension_path = ''

# 遍历文件名列表
for file_name in file_names:
    # 检查文件名是否以"/"结尾，表示该项是文件夹
    if file_name.endswith('/'):
        # 获取文件夹名称
        folder_name = os.path.basename(file_name[:-1])
        # 检查文件夹名称是否为"extension"
        if folder_name == 'extension':
            extension_path = file_name

print('extension from online path:', extension_path)



