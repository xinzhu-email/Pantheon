from bokeh.io import curdoc
from bokeh.models import Div
from Extension import Extension
import data as dt

def upload_callback():
    Extension()

def main(doc): 
    
    """starting page with loading remind"""
    dt.adata = dt.load_path()
    dt.init_data(dt.adata)
    print("main")
    loading_remind = Div(text='Loading data……')
    doc.add_root(loading_remind) 
    print('===loading finished=====')
    
    """update main page"""
    doc.add_next_tick_callback(upload_callback)                                                     

if __name__ == "main":
    main(curdoc())

 