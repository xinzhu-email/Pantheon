from bokeh.plotting import figure

class Plot:
    def __init__ (self, 
        **widgets):
        if widgets.get('source'):
            self.source = widgets.get('source')
        else:
            self.source = None
        self.plot = None
        self.glyphs = None
        self.plot_figure()

    def update_source(self, **widgets):
        self.source = widgets.get('source')
        self.plot_figure()
            
    def plot_figure (self):
        if self.source:
            plot = figure(width = 500, height = 500, tools = "pan,lasso_select,box_select,tap,wheel_zoom,save,hover")
            plot.xaxis.axis_label, plot.yaxis.axis_label = self.source.column_names[0], self.source.column_names[1]
            glyphs = plot.scatter(
                x = self.source.column_names[0],
                y = self.source.column_names[1],
                color = self.source.column_names[2],
                nonselection_alpha = 0.1,
                selection_line_color = 'black',
                selection_line_width = 0.5,
                source = self.source
            )
            self.glyphs = glyphs
            self.plot = plot
        else: 
            print("Fatal: Plot.__plot_figure: source not correctly inited")
            return