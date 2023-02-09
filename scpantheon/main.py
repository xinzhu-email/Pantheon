try:
    from scpantheon import source
except:
    import source
from bokeh.server.server import Server



# if __name__ == '__main__':
def run():
    print('Opening Bokeh application on http://localhost:5006/')
    server = Server({'/': source.main}, num_procs=1)
    server.start()
    server.io_loop.add_callback(server.show, "/")
    server.io_loop.start()
run()
print('ss')
# source.main()