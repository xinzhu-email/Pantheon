from scpantheon.buttons import make_layout, make_widget, Widget_type

class Console:
    def __init__(self):
        self.info = make_widget(Widget_type.div, text = "Debug Console:")
        self.layout = make_layout([self.info])