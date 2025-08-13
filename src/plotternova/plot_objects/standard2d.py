from abc import ABC, abstractmethod
import numpy as np
import numpy.typing as npt
from typing import Literal
from matplotlib.patches import Polygon


class Standard2dObject(ABC):
    """
    Base class for all allowed standard/basic 2D plot objects. Objects primarily for plottying x vs y,
    or for 1D histograms. Does not include specialized 2D plots like 2D histograms, matrix plots, etc.
    """
    pass

    @abstractmethod
    def draw():
        pass


class PointsLines(Standard2dObject):
    def __init__(self, 
                 xdata, 
                 ydata, 
                 label: str | None = None,
                 **kwargs) -> None:
        """
        Create points and/or lines plot objects that represent data.
        """
        self.xdata = xdata; self.ydata = ydata
        self.label = label

        # store **kwargs for plotting
        self.kwargs = kwargs

    def draw(self, ax) -> None:
        """
        Draws the histrogram on the supplied axes of BasicPlot or HistPlot objects
        """
        handle, = ax.plot(self.xdata, self.ydata, **self.kwargs)
        return handle


class ErrorBar(Standard2dObject):
    def __init__(self,
                 xdata: npt.ArrayLike,
                 ydata: npt.ArrayLike,
                 yerr: npt.ArrayLike,
                 label: str,
                 xerr: npt.ArrayLike | None = None,
                 **kwargs):
        self.xdata = xdata; self.ydata = ydata
        self.yerr = yerr
        self.label = label
        self.xerr = xerr if xerr is not None else None

        # store **kwargs for plotting histograms
        self.kwargs = kwargs

    def draw(self, ax) -> None:
        """
        Draws the data +/- error points on the supplied axes on a BasicPlot object
        """
        ax.errorbar(self.xdata, self.ydata)


class Hist(Standard2dObject):
    def __init__(self, 
                 data: npt.ArrayLike,
                 bins: int | npt.ArrayLike,
                 weights: npt.ArrayLike | None = None,
                 err: str | npt.ArrayLike | None = None, 
                 normalize: bool = False,
                 hist_type: str = "stepfilled",
                 err_type: Literal["ATLAS", "fillbetween", "errorbar"] = "ATLAS",
                 alpha: float = 1,
                 label: str | None = None,
                 **kwargs):
        """
        Creates histogram of data where the error can be supplied.

        Parameters:
        -----------
          - data: npt.ArrayLike of data to create a histogram for
          - bins: int or npt.ArrayLike. Passing an int requests for that many equally spaced bins
            from the min to max data values. Passing an ArrayLike is for custom bins.
          - weights: npt.ArrayLike for the weights to apply to each event.
          - err: str, npt.ArrayLike, or None. str options include "poisson", "standard", or ... 
            Passing in an ArrayLike, ensuring the same length as the bin count, assigns errors to 
            those bins. Passing None will not plot errors.
          - normalize: bool. Normalizes the histogram, default False.
          - hist_type: str, for various types of histogram appearances. Options include "bar",
            "step", and "stepfilled" (same as matplotlib ax.hist options). Defualts to
            "stepfilled".
          - err_type: str. Specifies the error type of a histogram if errors are to be plotted. Options
          - alpha: float, sets the opacity of a "filled" or "pattern" histogram. Defaults to 1 for 
            completely solid color. 0 corresponds to transparent.
          - label: name given to histogram to be shown in legend
          - kwargs: various other key-word arguments to matplotlib's ax.hist()
        """
        # store the data attributes
        self.data = data
        self.err = err; self.weights = weights
        self.normalize = normalize

        # store the bin attributes
        self.bins = bins

        # store the appearance attributes
        self.label = label
        self.hist_type = hist_type
        self.err_type = err_type
        self.alpha = alpha

        # store various other kwargs that go into plotting a histogram
        self.kwargs = kwargs

    def draw(self, ax):
        """
        Draws the histrogram on the supplied axes
        """
        n, bin_edges, handle = ax.hist(self.data, self.bins, density=self.normalize, histtype=self.hist_type, 
                          alpha=self.alpha, **self.kwargs)
    
        if self.err is not None:
            match self.err_type:
                case "ATLAS":
                    verts = []

                    # Upper edge
                    for i in range(len(bin_edges)-1):
                        binl = bin_edges[i]; binr = bin_edges[i+1]
                        y = n[i]
                        e = self.err[i]
                        verts.append((binl, y + e))
                        verts.append((binr, y + e))

                    # Lower edge (reversed)
                    for i in range(len(bin_edges)-1, 0, -1):
                        binl = bin_edges[i-1]; binr = bin_edges[i]
                        y = n[i-1]
                        e = self.err[i-1]
                        verts.append((binr, y - e))
                        verts.append((binl, y - e))

                    # Create polygon with hatching
                    poly = Polygon(verts, closed=True, facecolor='none', edgecolor='black', hatch='///////////', hatch_linewidth=0.5, linewidth=0)
                    ax.add_patch(poly)

                case "fillbetween":
                    ...

        return handle[0] # ax.hist() returns handles as a list here. Grabbing first element.


    def divide_hists(self, other, ax) -> npt.ArrayLike:
        """
        Method to divide one histogram's values by another. Meant to be plotted in a ratio plot, 
        below the main histogram plot, for example. Ensure both histograms have the same binning.
        """
        ...

    def display_stats(self, ax, sigma: float = 1):
        """
        Method to display the location of the mean and the +/- x*sigma from the mean for one hist. 
        """
        ...



class Step(Standard2dObject):
    def __init__(self):
        ...


class FillBetween(Standard2dObject):
    pass
