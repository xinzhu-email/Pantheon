# # -*- coding: utf-8 -*-
from multiprocessing import freeze_support
from multiprocessing import Process
from scpantheon.config import set_software_rendering
from scpantheon.front_end import data_qt
from scpantheon.app import bokeh_qt
import pkg_resources
import subprocess
import numpy as np
# import logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler("/home/zw/novellab/softwareUI/tutorial/logging_tutorial/log_scp.txt", mode="a"),
#         logging.StreamHandler()
#     ]
# )


if not hasattr(np, 'bool8'):
    np.bool8 = np.bool_

try: 
    import source
    from scpantheon.app import bokeh_qt
    from front_end import data_qt
    version = pkg_resources.get_distribution("scpantheon").version
except:
    print("pip install scpantheon")
    subprocess.check_call(['pip', 'install', "scpantheon"])
    from scpantheon import source
    from scpantheon.app import bokeh_qt
    from scpantheon.front_end import data_qt
    version = pkg_resources.get_distribution("scpantheon").version

from bokeh.server.server import Server
server = None

def run():
    global server
    print('Opening Bokeh application on http://localhost:5006/')
    server = Server({'/': source.main}, allow_websocket_origin=["localhost:5006"], port=5006) 
    server.start()  
    server.io_loop.start()
    server.show()

def app():
    global server
    if data_qt.main() == 'app closed':
        if bokeh_qt.main() == 'app closed':
            print('app ended')
    else: 
        print("app failed")
    p1.terminate()

def main():
    set_software_rendering()
    print("freeze support")
    freeze_support()
    global p1
    p1 = Process(target=run)
    p1.start()
    app()

if __name__ == '__main__':
    main()
