from bokeh.io import curdoc
from bokeh.models import Div
from Extension import Extension

def upload_callback():
    Extension()

def main(doc): 
    """store all data and widgets to show in the doc"""
    
    """starting page with loading remind"""
    loading_remind = Div(text='Loading data……')
    doc.add_root(loading_remind) 
    print('===loading finished=====')

    """init page"""
    # init data
    # Panel_Handler.get_extension()
    # Panel_Handler.init_modules()
    
    """update main page"""
    doc.add_next_tick_callback(upload_callback)                                                     

if __name__ == "main":
    main(curdoc())

 