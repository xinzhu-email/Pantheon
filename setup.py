from setuptools import setup

setup(
    name='scPANTHEON',# 需要打包的名字,即本模块要发布的名字
    version='0.0.18',#版本
    description='A graphical interface for single cell analysis.', # 简要描述
    packages=['scpantheon'],   #  需要打包的模块
    author='xinzhu', # 作者名
    author_email='xinzhu.jiang@sjtu.edu.cn',   # 作者邮件
    url='https://github.com/xinzhu-email/Pantheon', # 项目地址,一般是代码托管的网站
    install_requires=['bokeh','pandas','anndata','colorcet','scanpy','numpy'], # 依赖包,如果没有,可以不要
    entry_points={
        'console_scripts': [
            'sc-pantheon = scpantheon.main:run'
        ]
    },
    package_data={'scpantheon':['extension/*'],},
    license='MIT'
)