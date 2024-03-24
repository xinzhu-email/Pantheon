try:
    from scpantheon import sourceqt
except:
    import sourceqt

from bokeh.server.server import Server
import multiprocessing
import threading,time
import qt

def run():
    print('Opening Bokeh application on http://localhost:5006/')
    # sourceqt.qt_button()
    server = Server({'/': sourceqt.main},
                    allow_websocket_origin=["localhost:5006"], port=5006, show=False, num_procs=1) 
    server.start()  
    
    server.io_loop.start()

    server.show()


def app():
    global p1
    if qt.main() == 'app closed':
        p1.terminate()
        print('app ended')
    

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run)
    p1.start()
    app()

