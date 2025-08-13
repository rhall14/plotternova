from abc import ABC, abstractmethod
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt
from typing import List, Tuple
from .theme.style import STYLE_PRESETS; from .theme.color_theme import COLOR_THEMES
from .utils import *


class PlotBase(ABC):
    """
    The base class governing what attributes every plot should have and what standard methods every 
    plot type should contain. All other plot subclasses inherit from BasePlot.
    """
    def __init__(self,
                 ncol: int = 1,
                 nrow: int = 1,
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
                 beautify_ticks: bool = False,
                 title: str | None = None, 
                 dpi: int = 300,
                 style: str | dict = "default",
                 color_theme: str | dict = "light",
                 ):
        """
        The basic structure that every 2D plot is built on. Sets up a figure with the basic info
        needed to create a plot (i.e., title, axes, axes ticks, axes limits, labels, etc...)

        Parameters:
        -----------
          - nrow: int, specifies the number of plots to make in a row
          - ncol: int, specifies the number of plots to make in a column
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
          - beautify_ticks: bool. Calls a function to automatically attempt to make ticks nicer.
          - title: str or None, sets the title of the entire figure
          - dpi: int, sets the figure dpi
          - style: str or dict, defaults to "default". str options are "default", "publication",
            "publication small", "presentation", or "ATLAS", which are each presets for the style. 
            Otherwise, the user can pass in a dictionary of rcParams for complete customization.
          - color_theme: str or dict, defaults to "light". Sets the theme of the plots. Options are 
            "light", "dark", WILL ADD MORE LATER...
        """
        self.ncol = ncol; self.nrow = nrow

        # tick attributes
        self.xlim = xlim; self.ylim = ylim
        self.xticks = xticks; self.yticks = yticks
        self.xlog_on = xlog_on; self.ylog_on = ylog_on
        self.beautify_ticks = beautify_ticks

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

        # set the title attribute
        self.title = title
        
        self.dpi = dpi

        # store the style and color themes as attributes for later use
        self.style = style
        self.color_theme = color_theme

        # any relevant setting relating to font
        if isinstance(style, str):
            self.style_str = style
            self.style = STYLE_PRESETS.get(style, STYLE_PRESETS["default"])
        else:
            self.style_str = "custom"
            self.style = style  # assume dict
        
        # set the color theme of the plot
        if isinstance(color_theme, str):
            self.color_theme_str = color_theme
            self.color_theme = COLOR_THEMES.get(color_theme, {})
        else:
            self.color_theme_str = "custom"
            self.color_theme = color_theme


    def _setup_fig(self):
        """
        Perform an initial setup of the figure and axes, and performs some easy initial tasks like
        adding a grid, text, while leaving the rest of the setup that depends on the plotted data
        for later. 
        """
        # set the font style and math print with rcParams (still need to implement this feature)
        mpl.rcParams.update({**self.style, **self.color_theme})

        # initialize the mpl figure and axes with subplots
        self.fig, self.ax = plt.subplots(nrows=self.nrow, ncols=self.ncol, dpi=self.dpi)

        # apply tick adjustments
        if self.beautify_ticks:
            tick_adjuster(self.ax)

        # extra text to place on the plot
        if self.text_info is not None:
            add_text(self.ax, self.text_info)

        # grid
        if self.grid_style:
            print(self.grid_style)
            grid_adjuster(self.ax, self.grid_style)

        # set the title if present
        if self.title: self.ax.set_title(self.title)


    @abstractmethod
    def add_data(self):
        pass


    def apply_axes_settings(self,
                            xlabel,
                            ylabel,
                            xlim,
                            ylim,
                            xlog_on: bool = False,
                            ylog_on: bool = False):
        """
        Function designed to set the axes settings such as the labels, limits, and scale. Does not
        set the anything to do with axis ticks. See the tick_adjuster function for that purpose.
        """
        # labels
        if ("publication" in self.style_str) or ("ATLAS" in self.style_str):
                self.ax.set_xlabel(xlabel + "   ", loc="right")
                self.ax.set_ylabel(ylabel + "   ", loc="top")
        else:
            self.ax.set_xlabel(xlabel); self.ax.set_ylabel(ylabel)
        
        # set logarithmic axes if requested
        self.ax.set_xscale("log") if xlog_on else ...
        self.ax.set_yscale("log") if ylog_on else ...

        # set xy limits (if xlim/ylim specified, use those limits. Otherwise use auto limits)
        if xlim: self.ax.set_xlim(xlim[0], xlim[1])
        if ylim: self.ax.set_ylim(ylim[0], ylim[1])


    @abstractmethod
    def plot(self):
        pass


    def export(self, file_name, dpi=300, layout="tight", facecolor="white"):
        """
        Saves the plot in the file type of the user's choice, specified in the type extension in
        file_name (e.g., .pdf, and .png).
        """
        plt.savefig(file_name, dpi=dpi, bbox_inches=layout, facecolor=facecolor)
