from bokeh.models import TabPanel, Tabs
from bokeh.io import curdoc

def refresh(widget_id, new_layout):
    def refresh_traverse(widget_id, new_layout, _curroot=None):
        if _curroot is None:
            _curroot = curdoc().roots
        
        elif isinstance(_curroot, TabPanel):
            _curroot = [_curroot]
        
        for child in _curroot:
            if hasattr(child, 'children'):
                for i in range(len(child.children)):
                    if child.children[i].id == widget_id:
                        child.children[i] = new_layout
                        return True
                if refresh_traverse(widget_id, new_layout, child.children):
                    return True
            elif isinstance(child, Tabs):
                tab_substitute = False
                for tab in child.tabs:
                    if refresh_traverse(widget_id, new_layout, tab):
                        tab_substitute = True
                if tab_substitute:
                    return True
            elif isinstance(child, TabPanel):
                for i in range(len(child.child.children)):
                    if hasattr(child.child.children[i], 'id') and child.child.children[i].id == widget_id:
                        child.child.children[i] = new_layout
                        return True
                if refresh_traverse(widget_id, new_layout, child.child.children):
                    return True
        return False
    
    found = refresh_traverse(widget_id, new_layout)
    if found == False:
        print("Error: no corresponding id")


def refresh_layout(widget_id, new_layout, target_layout):
    def refresh_traverse(widget_id, new_layout, target_layout):
        if hasattr(target_layout, 'id') and target_layout.id == widget_id:
            target_layout = new_layout
            return
        elif hasattr(target_layout, 'children'):
            target = target_layout.children
        elif isinstance(target_layout, list):
            target = target_layout
        for child in target:
            if hasattr(child, 'children'):
                for i in range(len(child.children)):
                    if child.children[i].id == widget_id:
                        child.children[i] = new_layout
                        return True
                if refresh_traverse(widget_id, new_layout, child.children):
                    return True
            elif isinstance(child, Tabs):
                if refresh_traverse(widget_id, new_layout, child.tabs):
                    return True
            elif isinstance(child, TabPanel):
                if refresh_traverse(widget_id, new_layout, child.child.children):
                    return True
        return False
    
    found = refresh_traverse(widget_id, new_layout, target_layout)
    if found == False:
        print("Error: no corresponding id")