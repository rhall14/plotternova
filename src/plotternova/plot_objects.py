import numpy as np
import numpy.typing as npt


# every plot objets must have a draw method supplied with axes to be plotted on

class PointsLines:
    def __init__(self, 
                 xdata, 
                 ydata, 
                 label,
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


class ErrorBar:
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


class Hist:
    def __init__(self, 
                 data: npt.ArrayLike, 
                 label: str, 
                 bins: npt.ArrayLike,
                 err: str | npt.ArrayLike | None = None, 
                 **kwargs):
        """
        Creates histogram of data where the error can be supplied.
        """
        self.data = data
        self.label = label
        self.err = err
        
        # store the bin attributes
        self.bins = bins

        # store various other kwargs that go into plotting a histogram
        self.kwargs = kwargs

    def draw(self, ax) -> None:
        """
        Draws the histrogram on the supplied axes
        """
        handle, = ax.hist(self.data)

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



class Step:
    def __init__(self):
        ...


class FillBetween:
    pass


class Contour:
    pass


class Matrix:
    pass


class HeatMap:
    pass