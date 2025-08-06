from ..core import PlotBase
from ..plot_objects import PointsLines, Hist, FillBetween
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from ..utils import *
from typing import List, Tuple


class BasicPlot(PlotBase):
    """
    Class for creating basic plots with points, lines, or fill-between.
    """
    
    def __init__(self,
                 xlim = None,
                 ylim = None,
                 xticks = None,
                 yticks = None,
                 xlog_on = False,
                 ylog_on = False,
                 xlabel = "x",
                 ylabel = "y",
                 text_info: List[dict] | None = None,
                 legend_settings: None | str | dict = "default_inside",
                 grid_on = False,
                 **kwargs):
        """
        Constructor for a BasicPlot object. This plot specializes in quick y vs x plots and is
        flexible for plotting multple data sets with quick formatting.

        Parameters:
        -----------
        """
        # initialize first as instance of PlotBase class
        super().__init__(**kwargs)

        # initialize the figure (without anything plotted yet)
        self._setup_fig()

        # assign the BasicPlot attriubtes
        # -------------------------------
        # tick attributes
        self.xlim = xlim; self.ylim = ylim
        self.xticks = xticks; self.yticks = yticks
        self.xlog_on = xlog_on; self.ylog_on = ylog_on

        # grid attributes
        self.grid_on = grid_on

        # xy label attributes
        self.xlabel = xlabel; self.ylabel = ylabel

        # extra text attribute
        self.text_info = text_info

        # legend attriubtes
        if legend_settings is not None:
            self.legend_on = True
            self.legend_settings = legend_settings
        else:
            self.legend_on = False

        # initialize a datasets attribute to store data to plot
        self._datasets = []

        # initialize handles and labels for plotted objects
        self.legend_handles = []; self.legend_labels = []


    def add_data(self, x_data, y_data, label, object_type="pointslines", **kwargs):
        """
        Add data to the plot, with the option to choose the type/format the data should be plotted
        in. Adds data in the form of the three Points, Line, and FillBetween objects.
        """
        match object_type.lower():
            case "points" | "line" | "pointslines":
                self._datasets.append(PointsLines(x_data, y_data, label, **kwargs))
                self.legend_handles

            case "hist":
                self._datasets.append(Hist())

            case "fillbetween":
                y_low, y_mid, y_high = y_data
                self._datasets.append(FillBetween(x_data, y_low, y_mid, y_high))

            case _:
                print(f"Warning: {object_type} is an unkown data type! Check documentation for " +
                      "allowed data types.")


    def remove_data(self):
        pass

    
    def plot(self, export=False, file_name="default.png", **kwargs):
        """
        Creates and shows a plot in a separate window once the data has been added and the necessary
        plot configurations have been made.
        """
        # ----------------------------------------------------------------
        # plotting all of the added datasets
        # ----------------------------------------------------------------
        minx_arr = []; maxx_arr = []; miny_arr = []; maxy_arr = []
        for dataset in self._datasets:
            handle = dataset.draw(self.ax)
            label = dataset.label

            # store the legend handles and labels
            self.legend_handles.append(handle)
            self.legend_labels.append(label)

            # computing the min and max values for autosetting axis limits
            minx_arr.append(np.min(dataset.xdata))
            maxx_arr.append(np.max(dataset.xdata))
            miny_arr.append(np.min(dataset.ydata))
            maxy_arr.append(np.max(dataset.ydata))

        # ----------------------------------------------------------------
        # adjusting the axes settings
        # ----------------------------------------------------------------
        # compute the x and y limits to apply if no limits were provided
        if self.xlim is None:
            xlow = magnitude_round(np.min(minx_arr), type="floor") if self.xlog_on else np.min(minx_arr)
            xhigh = magnitude_round(np.max(maxx_arr), type="ceil") if self.xlog_on else np.max(maxx_arr)

            if self.xlog_on:
                self.xlim = [xlow, xhigh]
            else:
                xrange = xhigh - xlow
                self.xlim = [xlow-0.04*xrange, xhigh+0.04*xrange]

        if self.ylim is None:
            ylow = magnitude_round(np.min(miny_arr), type="floor") if self.ylog_on else np.min(miny_arr)
            yhigh = magnitude_round(np.max(maxy_arr), type="ceil") if self.ylog_on else np.max(maxy_arr)

            if self.ylog_on:
                self.ylim = [ylow, yhigh]
            else:
                yrange = yhigh - ylow
                self.ylim = [ylow-0.04*yrange, yhigh+0.04*yrange]


        # apply the settings to the axes
        self.apply_axes_settings(self.xlabel, self.ylabel, self.xlim, self.ylim, self.xlog_on, 
                                 self.ylog_on)

        # apply tick adjustments
        tick_adjuster(self.ax)

        # legend
        if self.legend_on:
            decorate_legend(self.ax, self.legend_handles, self.legend_labels,
                            settings = self.legend_settings)

        # extra text to place on the plot
        if self.text_info is not None:
            for text_info_dict in self.text_info:
                text = text_info_dict["text"]
                coords = text_info_dict["coords"]

                # create a filtered dictionary without the text and coordinates
                exclude = ["text", "coords"]
                filtered_dict = {k: v for k, v in text_info_dict.items() if k not in exclude}
                
                self.ax.text(coords[0], coords[1], text, transform=self.ax.transAxes, **filtered_dict)

        # grid
        if self.grid_on:
            self.ax.grid()

        # optional saving of the figure
        if export:
            self.export(file_name="test_basic.png", **kwargs)

        plt.show()

        # restore plotting defaults
        mpl.style.use('default')