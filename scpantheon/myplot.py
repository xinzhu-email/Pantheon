from bokeh.plotting import figure
from bokeh.models import LogColorMapper, ColorBar
from bokeh.transform import linear_cmap
import colorcet as cc

class Plot:
    def __init__ (self, 
        is_marker: bool | None = False,
        **widgets
        ):
        self.is_marker = is_marker
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
            if self.is_marker:
                color_mapper = LogColorMapper(
                    palette = cc.kbc[::-1], 
                    low = min(self.source.data['color']), 
                    high = max(self.source.data['color'])
                    )
                glyphs = plot.scatter(
                    x = self.source.column_names[0],
                    y = self.source.column_names[-2],
                    source = self.source,
                    color = linear_cmap(
                        'color',
                        palette = cc.kbc[::-1],
                        low = min(self.source.data['color']),
                        high = max(self.source.data['color']),
                        ),
                    nonselection_alpha = 0.1,
                    selection_line_color = 'black',
                    selection_line_width = 0.5,
                    # source = self.source
                    )
                color_bar = ColorBar(color_mapper=color_mapper, location=(0, 0))
                plot.add_layout(color_bar, 'right')

            else:
                glyphs = plot.scatter(
                    x = self.source.column_names[0],
                    y = self.source.column_names[-2],
                    color = self.source.column_names[-1],
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