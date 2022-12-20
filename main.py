try:
    from scpantheon import sourceqt
except:
    import sourceqt

from bokeh.server.server import Server
import multiprocessing
import threading,time
import qt

def run():
    # global lock
    # lock.acquire()
    print('Opening Bokeh application on http://localhost:5006/')
    # sourceqt.qt_button()
    server = Server({'/': sourceqt.main},
                    allow_websocket_origin=["localhost:5006"], port=5006, show=False, num_procs=1) 
    server.start()  
    # lock.release()    
    # server.io_loop.add_callback(server.show, "/")
    
    server.io_loop.start()

def app():
    qt.main()

if __name__ == '__main__':
    # global lock
    p1 = multiprocessing.Process(target=run)
    p2 = multiprocessing.Process(target=app)
    p1.start()
    p2.start()

    p1.join()
    p2.join()
    '''lock = threading.Lock()
    t1 = threading.Thread(target=run)
    t2 = threading.Thread(target=app)

    t1.start()
    t2.start()

    t1.join()
    t2.join()'''

'''

问题：把数据传到 server 里

'''
