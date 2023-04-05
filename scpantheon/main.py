from multiprocessing import freeze_support
freeze_support()

import warnings

from bokeh.server.server import Server
import multiprocessing
import warnings

class InstallWarning(Warning):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return repr(self.message)

import qt, source

'''try: 
    from scpantheon import qt, source # import from online
except:
    warnings.warn('YOU HAVE TO INSTALL PyQt5',InstallWarning)'''

def run():
    global server
    print('Opening Bokeh application on http://localhost:5006/')
    server = Server({'/': source.main},
                    allow_websocket_origin=["localhost:5006"], port=5006, show=False, num_procs=1) 
    server.start()  
    server.io_loop.start()
    server.show()

def app():
    if qt.main() == 'app closed':
        p1.terminate()
        print('app ended')
    

def main():
    global p1
    p1 = multiprocessing.Process(target=run)
    p1.start()
    app()


if __name__ == '__main__':
    main()