from ..core import PlotBase
from ..plot_objects.standard2d import Standard2dObject, PointsLines, Hist, ErrorBar, FillBetween
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from ..utils import *
from typing import List, Tuple, Literal


class HistPlot(PlotBase):
    """
    Class for creating histogram plots with points, lines, or fill-between.
    """

    ALLOWED_TYPES = (Hist, PointsLines, ErrorBar, FillBetween)
    
    def __init__(self,
                 stack: bool = False,
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

        self.stack = stack
        self.ratio = ratio


    def add_data(self, *plot_objects: Standard2dObject) -> None:
        """
        Add data to the plot, with the option to choose the type/format the data should be plotted
        in. Can add data as hists, points/lines, errorbars, or fill-between objects.

        Parameters:
        -----------
          - *plot_objects: one or more plot objects to add to the figure. 
        """
        for plot_object in plot_objects:
            if not isinstance(plot_object, HistPlot.ALLOWED_TYPES):
                raise TypeError(
                    f"Invalid plot type: {type(plot_object).__name__}. "
                    f"Allowed types for histograms: {[cls.__name__ for cls in self.ALLOWED_TYPES]}"
                )
            else:
                self._datasets.append(plot_object)

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
            
            # determine the max and min x and y values for the data
            if isinstance(dataset, Hist):
                minx_arr.append(np.min(dataset.bins))
                maxx_arr.append(np.max(dataset.bins))
            elif isinstance(dataset, PointsLines):
                minx_arr.append(np.min(dataset.xdata))
                maxx_arr.append(np.max(dataset.xdata))
                miny_arr.append(np.min(dataset.ydata))
                maxy_arr.append(np.max(dataset.ydata))
            elif isinstance(dataset, ErrorBar):
                ...
            elif isinstance(dataset, FillBetween):
                ...

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

        # if self.ylim is None:
        #     self.ylim = compute_auto_limits(miny_arr, maxy_arr, log=self.ylog_on)

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