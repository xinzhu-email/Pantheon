from setuptools import setup
import setuptools

# python setup.py sdist bdist_wheel
# python -m twine upload dist/*

setup(
    name='scPANTHEON',# 需要打包的名字,即本模块要发布的名字
    version='0.2.4',#版本
    description='A graphical interface for single cell analysis.', # 简要描述
    packages=['scpantheon'],   #  需要打包的模块
    author='xinzhu', # 作者名
    author_email='xinzhu.jiang@sjtu.edu.cn',   # 作者邮件
    url='https://github.com/xinzhu-email/Pantheon', # 项目地址,一般是代码托管的网站
    install_requires=['bokeh==2.4.3','pandas','anndata==0.8.0','colorcet','scanpy','numpy','PyQt5==5.15.9','PyQtWebEngine==5.15.6','appdirs==1.4.4'], # 依赖包,如果没有,可以不要
    extras_require={
        'tomas': ['tomas'],
    }, # 依赖包,深度使用需手动安装
    entry_points={
        'console_scripts': [
            'sc-pantheon = scpantheon.main:main' # scripts -> multiprocessing
        ]
    },
    package_data={'scpantheon':['extension/*'],},
    license='MIT'
)