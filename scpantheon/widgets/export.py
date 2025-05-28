from scpantheon.buttons import make_layout, make_widget, Widget_type

class Export:
    def __init__(self):
        self.init_widgets()
        self.layout = self.init_layout()
    
    def init_widgets(self):
        self.title = make_widget(Widget_type.div, text = "<div style='font-size: 40px;'>Export")
        self.mode = make_widget(
            Widget_type.select, 
            lambda: self.mode_callback(),
            options = [".h5ad file with data only", ".scp file with current UI"],
            value = ".h5ad file with data only"
            )
        self.confirm = make_widget(
            Widget_type.button,
            lambda: self.confirm_callback(),
            label = "Export"
        )

    def init_layout(self):
        return make_layout([self.title, self.mode, self.confirm])


    def mode_callback(self):
        pass

    def confirm_callback(self):
        pass