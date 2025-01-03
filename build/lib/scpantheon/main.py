<<<<<<< HEAD
'''from multiprocessing import freeze_support
freeze_support()'''

from bokeh.server.server import Server
import multiprocessing
import warnings
try:
    from scpantheon.app import bokeh_qt
    from scpantheon.front_end import data_qt
except:
    from scpantheon.app import bokeh_qt
    import data_qt

class ImportWarning(Warning):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

try: 
    from scpantheon import source
except:
    from scpantheon import source # import from online
    warnings.warn('source import failed',ImportWarning)
=======
# -*- coding: utf-8 -*-

from multiprocessing import freeze_support
import multiprocessing
import pkg_resources
import subprocess
from scpantheon import source
from scpantheon.app import bokeh_qt
from scpantheon.front_end import data_qt
from bokeh.server.server import Server
import sys

version = pkg_resources.get_distribution("scpantheon").version
server = None  # 声明全局变量 server
>>>>>>> extension

def run():
    global server
    print('Opening Bokeh application on http://localhost:5006/')
    server = Server({'/': source.main}, allow_websocket_origin=["localhost:5006"], port=5006, show=False, num_procs=1) 
    server.start()  
    server.io_loop.start()
    server.show()

def app():
<<<<<<< HEAD
    if data_qt.main() == 'app closed':
        print('choosing finished')
        if bokeh_qt.main() == 'app closed':
            p1.terminate()
            print('app ended')
    else: 
        p1.terminate()
        print("app ended")
    

def main():
=======
    global server
    if data_qt.main() == 'app closed':
        if bokeh_qt.main() == 'app closed':
            print('app ended')
    else: 
        print("app failed")
    p1.terminate()

def main():
    print("freeze support")
    freeze_support()
>>>>>>> extension
    global p1
    p1 = multiprocessing.Process(target=run)
    p1.start()
    app()

<<<<<<< HEAD

if __name__ == '__main__':
    main()
=======
if __name__ == '__main__':
    main()
>>>>>>> extension
