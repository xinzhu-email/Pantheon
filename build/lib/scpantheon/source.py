from bokeh.io import curdoc
from bokeh.models import Div
from Extension import Extension

def upload_callback():
    Extension()

def main(doc): 
    
    """starting page with loading remind"""
    loading_remind = Div(text='Loading data……')
    doc.add_root(loading_remind) 
    print('===loading finished=====')
    
    """update main page"""
    doc.add_next_tick_callback(upload_callback)                                                     

if __name__ == "main":
    main(curdoc())
