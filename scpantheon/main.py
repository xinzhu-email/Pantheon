from multiprocessing import freeze_support

import multiprocessing
import pkg_resources, subprocess
try: 
    # !!! from scpantheon import source
    import source
    from scpantheon.app import bokeh_qt
    # !!! from scpantheon.front_end import data_qt
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

def run():
    global server
    print('Opening Bokeh application on http://localhost:5006/')
    server = Server({'/': source.main}, allow_websocket_origin=["localhost:5006"], port=5006, show=False, num_procs=1) 
    server.start()  
    server.io_loop.start()
    server.show()

def app():
    if data_qt.main() == 'app closed':
        if bokeh_qt.main() == 'app closed':
            print('app ended')
    else: 
        print("app failed")
    p1.terminate()

if __name__ == '__main__':
    print("freeze support")
    freeze_support()
    global p1
    p1 = multiprocessing.Process(target=run)
    p1.start()
    app()

