from ..core import PlotBase
from ..plot_objects import PointsLines, Hist, FillBetween
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
                 xlim: Tuple[float, float] | None = None,
                 ylim: Tuple[float, float] | None = None,
                 xticks: npt.ArrayLike | None = None,
                 yticks: npt.ArrayLike | None = None,
                 xlog_on: bool = False,
                 ylog_on: bool = False,
                 xlabel: str = "x",
                 ylabel: str = "y",
                 text_info: List[dict] | None = None,
                 legend_settings: None | str | dict = "default_inside",
                 grid_style: str | None = None,
                 **kwargs):
        """
        Constructor for a BasicPlot object. This plot specializes in quick y vs x plots and is
        flexible for plotting multple data sets with quick formatting.

        Parameters:
        -----------
          - xlim/ylim: 2-tuple of lower and upper x, y limits. Default 'None' will use auto limits.
          - xticks/yticks: array-like object containing location of major ticks. Defualt ticks when
            'None' passed
          - xlog_on/ylog_on: boolean enabling or disabling logarithmic axes
          - xlabel/ylabel: str the x and y labels. Can pass in latex formatted strings for mathprint
          - text_info: list of dictionaries. Defaults to 'None' if no text to be displayed. Each 
            dictionary contains information for each piece of text and has the following parameters:
            * "text": string of the text to add to the plot
            * "coords": 2-tuple of the coordinates on where to place the text on the axes
            * any other kwargs to pass into ax.text() (see matplotlib ax.text() for full options)
          - legend_settings: Can take 3 possible arguments:
            * None: will not create a legend
            * str: choose quick available legend presets. Default is "default_inside". See 
              utils.decorate_legend() for full list of presets.
            * dict: for full customization, can pass in desired kwargs as a dict for ax.legend()
          - grid_style: Defaults to None which does not activate the grid. Otherwise, pass in a str
            for various presets. See utils.grid_adjuster() for various preset types
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

        # assign the BasicPlot attriubtes
        # -------------------------------
        # tick attributes
        self.xlim = xlim; self.ylim = ylim
        self.xticks = xticks; self.yticks = yticks
        self.xlog_on = xlog_on; self.ylog_on = ylog_on

        # grid attributes
        self.grid_style = grid_style

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
            self.xlim = compute_auto_limits(minx_arr, maxx_arr, log=self.xlog_on)

        if self.ylim is None:
            self.ylim = compute_auto_limits(miny_arr, maxy_arr, log=self.ylog_on)

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
            add_text(self.ax, self.text_info)

        # grid
        if self.grid_style:
            print(self.grid_style)
            grid_adjuster(self.ax, self.grid_style)

        # optional saving of the figure
        if export:
            self.export(file_name=file_name, **kwargs)

        plt.show()

        # restore plotting defaults
        mpl.style.use('default')