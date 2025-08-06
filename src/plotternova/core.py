from abc import ABC, abstractmethod
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from .theme.style import STYLE_PRESETS; from .theme.color_theme import COLOR_THEMES


class PlotBase(ABC):
    """
    The base class governing what attributes every plot should have and what standard methods every 
    plot type should contain. All other plot subclasses inherit from BasePlot.
    """
    def __init__(self,
                 ncol = 1,
                 nrow = 1,
                 title = None, 
                 dpi = 300,
                 style: str | dict = "default",
                 color_theme: str | dict = "light",
                 ):
        self.ncol = ncol; self.nrow = nrow

        # set the figure title attribute
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
        Perform an initial setup of the figure and axes
        """
        # set the font style and math print with rcParams (still need to implement this feature)
        mpl.rcParams.update({**self.style, **self.color_theme})

        # initialize the mpl figure and axes with subplots
        self.fig, self.ax = plt.subplots(nrows=self.nrow, ncols=self.ncol, dpi=self.dpi)

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
        self.ax.set_xlim(xlim[0], xlim[1]); self.ax.set_ylim(ylim[0], ylim[1])


    @abstractmethod
    def plot(self):
        pass


    def export(self, file_name, dpi=300, layout="tight", facecolor="white"):
        """
        Saves the plot in the file type of the user's choice, specified in the type extension in
        file_name (e.g., .pdf, and .png).
        """
        plt.savefig(file_name, dpi=dpi, bbox_inches=layout, facecolor=facecolor)
