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
    from scpantheon.front_end import data_qt

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

def run():
    global server
    print('Opening Bokeh application on http://localhost:5006/')
    server = Server({'/': source.main}, allow_websocket_origin=["localhost:5006"], port=5006, show=False, num_procs=1) 
    server.start()  
    server.io_loop.start()
    server.show()

def app():
    if data_qt.main() == 'app closed':
        print('choosing finished')
        if bokeh_qt.main() == 'app closed':
            p1.terminate()
            print('app ended')
    else: 
        p1.terminate()
        print("app ended")
    

def main():
    global p1
    p1 = multiprocessing.Process(target=run)
    p1.start()
    app()


if __name__ == '__main__':
    main()