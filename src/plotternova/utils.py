import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator
import numpy as np
from typing import List, Tuple


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


def add_text(ax, text_dicts: List[dict]):
    for text_dict in text_dicts:
        text = text_dict["text"]
        coords = text_dict["coords"]

        # if the user specifies "transform" = True, then ax.text expects normalized coordinates
        if ("transform" in text_dict) and (text_dict["transform"] == True):
            # create a filtered dictionary without the text and coordinates
            exclude = ["text", "coords", "transform"]
            filtered_dict = {k: v for k, v in text_dict.items() if k not in exclude}
            ax.text(coords[0], coords[1], text, transform=ax.transAxes, **filtered_dict)

        # otherwise, the coordinates are using the actual axes coordinates
        else:
            # create a filtered dictionary without the text and coordinates
            exclude = ["text", "coords"]
            filtered_dict = {k: v for k, v in text_dict.items() if k not in exclude}
            ax.text(coords[0], coords[1], text, **filtered_dict)


def grid_adjuster(ax, preset: str = "line", logx: bool = False, logy: bool = False):
    """
    Activates the grid for a 2D plot

    Parameters:
    -----------
      - ax: the axes to activate the grid on
      - preset: str for the grid preset. The format for a preset is 'major_type'-'minor_type', where
        "line", "dash", and "dot" are the options for each. The following are the available presets:
        * "line": grid lines are lines along only the major ticks
        * "dash": grid lines are dashes along only the major ticks
        * "dot": grid lines are dots along only the major ticks
        * "line-line": major and minor grid lines are lines
        * "dash-dash": major and minor grid lines are dashes
        * "dot-dot": major and minor grid lines are dots
        * any other permutatation of "line", "dash", and "dot"
    """
    settings = preset.split("-")

    options = {"line": "-", "dash": "--", "dot": ":"}

    if not all(grid_type in list(options.keys()) for grid_type in settings):
        print("Warning: invalid grid option requested. Types are only 'line', 'dash, and 'dot'. " +
              "Disabling grid...")
        return None


    match len(settings):
        case 1:
            ax.grid(which="major", linestyle=options[settings[0]], linewidth=0.5, c="black",
                    alpha=0.5)

        case 2:
            ax.grid(which="major", linestyle=options[settings[0]], linewidth=0.5, c="grey", 
                    alpha=0.6)
            ax.grid(which="minor", linestyle=options[settings[1]], linewidth=0.25, c="grey", 
                    alpha=0.5)

        case _:
            print(f"Warning: {str} not a valid preset. Can at most activate grid lines for major " +
                  "and minor ticks. Cannot have 'line-line-line' for example.")


def compute_auto_limits(min_arr: List[float], max_arr: List[float], log: bool = False):
    low = magnitude_round(np.min(min_arr), type="floor") if log else np.min(min_arr)
    high = magnitude_round(np.max(max_arr), type="ceil") if log else np.max(max_arr)

    if log:
        return [low, high]
    else:
        span = high - low
        return [low-0.04*span, high+0.04*span]


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