from ..core import PlotBase
from ..plot_objects.standard2d import PointsLines, Hist, FillBetween
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from ..utils import *
from typing import List, Tuple


class BasicPlot(PlotBase):
    """
    Class for creating basic plots with points, lines, or fill-between.
    """
    
    def __init__(self,
                 **kwargs):
        """
        Constructor for a BasicPlot object. This plot specializes in quick y vs x plots and is
        flexible for plotting multple data sets with quick formatting.

        Parameters:
        -----------
          - **kwargs: keyword arguments for the BasePlot constructor

        Generates:
        ----------
            Skeleton figure with all of the various settings stored as attributes, ready for plotting
            with BasicPlot.plot()
        """
        # initialize first as instance of PlotBase class
        super().__init__(**kwargs)

        # initialize the figure (without anything plotted yet)
        self._setup_fig()


    def add_data(self, x_data, y_data, label, object_type="pointslines", **kwargs):
        """
        Add data to the plot, with the option to choose the type/format the data should be plotted
        in. Adds data in the form of the three Points, Line, and FillBetween objects.
        """
        match object_type.lower():
            case "points" | "line" | "pointslines":
                self._datasets.append(PointsLines(x_data, y_data, label, **kwargs))

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
            self.xlim = compute_auto_limits(minx_arr, maxx_arr, log=self.xlog_on)

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