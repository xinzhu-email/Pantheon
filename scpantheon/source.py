from bokeh.io import curdoc
from bokeh.models import Div
from scpantheon.framework import Framework
import stdata as dt
from scpantheon.stdata import ValidCache
import logging
logger = logging.getLogger(__name__)

def upload_callback():
    Framework()

def main(doc): 
    
    """starting page with loading remind"""
    loading_remind = Div(text='Loading data……')
    dt.adata = dt.init_data()
    dt.validcache = ValidCache(dt.adata)
    doc.add_root(loading_remind)
    doc.clear() 
    print('===loading finished=====')
    
    """update main page"""
    doc.add_next_tick_callback(upload_callback)                                                     

if __name__ == "main":
    main(curdoc())
