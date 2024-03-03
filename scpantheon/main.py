from multiprocessing import freeze_support
freeze_support()

from bokeh.server.server import Server
import multiprocessing
import warnings

try: 
    # !!!
    from app import bokeh_qt
    from front_end import data_qt
except:
    from app import bokeh_qt
    from front_end import data_qt

class ImportWarning(Warning):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

try:  
    # !!!
    import source
except:
    import source # import from online
    warnings.warn('source import failed',ImportWarning)
 
global dir

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

def main():
    global p1
    p1 = multiprocessing.Process(target=run)
    p1.start()
    app()


if __name__ == '__main__':
    main()