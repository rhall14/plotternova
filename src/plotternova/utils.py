import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator
import numpy as np


def decorate_legend(ax, handles, labels, settings, fontsize=mpl.rcParams["legend.fontsize"]):
        """
        Method to be called before plot(), which offers more customizable legend adjustments.
        """
        # if the user chose one of the predefined legend styles
        if type(settings) == str:
            match settings:
                case "default inside":
                    ax.legend(handles, labels, loc=0, fontsize=fontsize, frameon=False)

                case "default outside":
                    ax.legend(handles, labels, loc="upper left", bbox_to_anchor=(1, 1),
                              fontsize=fontsize, frameon=False)

                case "fancy inside":
                    print("have not implemented yet :(")
        
                case "fancy_outside":
                    print("have not implemented yet :(")

                case _:
                    print(f"Warning: {settings} is an invalid legend settings type! Check " +
                           "documentation for available legend presets.")

        # if the user passed in a dictionary of legend settings for full custonmization
        else:
            ax.legend(handles, labels, **settings)


def tick_adjuster(ax,
                  xticks = None,
                  yticks = None, 
                  logx = False, 
                  logy = False):
    ax.minorticks_on()
    if xticks:
        ax.set_xticks(xticks)
    if yticks:
        ax.set_yticks(yticks)
    ax.tick_params(direction='in', top=True, right=True)


def grid_adjuster(ax):
    ...


def magnitude_round(x, type="ceil"):
    if type == "ceil":
        return 10**(np.ceil(np.log10(x)))
    elif type == "floor":
        return 10**(np.floor(np.log10(x)))


def validate_xy(x, y):
    x = np.asarray(x)
    y = np.asarray(y)
    if x.shape != y.shape:
        raise ValueError(f"x and y must have the same shape, got {x.shape} and {y.shape}")
    return x, y