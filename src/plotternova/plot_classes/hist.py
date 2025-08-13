from ..core import PlotBase
from ..plot_objects import PointsLines, Hist
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from ..utils import *
from typing import List, Tuple


class HistPlot(PlotBase):
    """
    Class for creating histogram plots with points, lines, or fill-between.
    """
    
    def __init__(self,
                 hist_type: str = "stepfilled",
                 normalize: bool = False,
                 stack: bool = False,
                 alpha: float = 1,
                 ratio: bool = False,
                 **kwargs):
        """
        Constructor for a HistPlot object. This plot specializes in generating plots for neatly 
        displaying multiple histograms with various mechanisms for comparison appearance.

        Parameters:
        -----------
          - 

        Generates:
        ----------
            Skeleton figure with all of the various settings stored as attributes, ready for plotting
            with HistPlot.plot()
        """
        # initialize first as instance of PlotBase class
        super().__init__(**kwargs)

        # initialize the figure (without anything plotted yet)
        self._setup_fig()

        self.hist_type = hist_type
        self.normalize = normalize
        self.stack = stack
        self.alpha = alpha
        self.ratio = ratio



    '''
    NOTE: CHANGE THIS TO BE A FUNCTION FOR EACH PLOT_OBJECT TYPE!!! I.E., ADD_POINTSLINES, ADD_HIST,
          ADD_ERRBAR, ETC...
    '''
    def add_data(self, x_data, y_data, label, object_type="pointslines", **kwargs):
        """
        Add data to the plot, with the option to choose the type/format the data should be plotted
        in. Adds data in the form of the Hist, Points, and Line objects.
        """
        match object_type.lower():
            case "hist":
                self._datasets.append(Hist())

            case "points" | "line" | "pointslines":
                self._datasets.append(PointsLines(x_data, y_data, label, **kwargs))
                self.legend_handles

            case _:
                print(f"Warning: {object_type} is an unkown data type! Check documentation for " +
                      "allowed data types.")


    def remove_data(self):
        pass

    def _stack_hists(self):
        """
        Stacks all of the stored histograms in self._datasets, plot each hist on top of each other.
        """
        ...

    def _plot_ratio(self):
        """
        If a ratio plot is requested, this method handles plotting it. It is used in plot()
        """
        ...

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
            if label:
                self.legend_handles.append(handle)
                self.legend_labels.append(label)

        # ----------------------------------------------------------------
        # adjusting the axes settings
        # ----------------------------------------------------------------
        # compute the x and y limits to apply if no limits were provided
        if self.xlim is None:
            self.xlim = compute_auto_limits(minx_arr, maxx_arr)

        if self.ylim is None:
            self.ylim = compute_auto_limits(miny_arr, maxy_arr, log=self.ylog_on)

        # apply the settings to the axes
        self.apply_axes_settings(self.xlabel, self.ylabel, self.xlim, self.ylim, self.xlog_on, 
                                 self.ylog_on)

        # legend
        if self.legend_on:
            decorate_legend(self.ax, self.legend_handles, self.legend_labels,
                            settings = self.legend_settings)

        # optional saving of the figure
        if export:
            self.export(file_name=file_name, **kwargs)

        plt.show()

        # restore plotting defaults
        mpl.style.use('default')