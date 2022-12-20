try:
    from scpantheon import sourceqt
except:
    import sourceqt

from bokeh.server.server import Server
import multiprocessing, threading
import qt
import ctypes 


def run():      
    print('Opening Bokeh application on http://localhost:5006/')
    # sourceqt.qt_button()
    server = Server({'/': sourceqt.main},
                    allow_websocket_origin=["localhost:5006"], port=5006, show=False, num_procs=1) 
    server.start()      
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
run()