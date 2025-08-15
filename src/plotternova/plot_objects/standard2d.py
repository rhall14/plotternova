from abc import ABC, abstractmethod
import numpy as np
import numpy.typing as npt
from typing import Literal, Tuple
from matplotlib.patches import Polygon
from ..utils import check_shape


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
                 label: str | None = None,
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
        ax.errorbar(self.xdata, self.ydata, yerr=self.yerr, elinewidth=1, capsize=1, **self.kwargs)


class Hist(Standard2dObject):
    def __init__(self, 
                 data: npt.ArrayLike,
                 bins: int | npt.ArrayLike,
                 bin_range: Tuple[float, float] | None = None,
                 counted: bool = False,
                 weights: npt.ArrayLike | None = None,
                 include_error: bool = False,
                 normalize: bool = False,
                 hist_type: Literal["stepfilled", "step", "bar", "point"] = "stepfilled",
                 err_style: Literal["ATLAS", "fillbetween", "errorbar"] = "ATLAS",
                 alpha: float = 1,
                 label: str | None = None,
                 **kwargs):
        """
        Creates histogram of data where the error can be supplied.

        Parameters:
        -----------
          - data: npt.ArrayLike of data to create a histogram for. You can pass in the raw data or 
            the already counted up data in the specified bins. If data is already counted, pass 
            counted = True.
          - bins: int or npt.ArrayLike. Passing an int requests for that many equally spaced bins
            from the min to max data values. Passing an ArrayLike is for specifying bin edges. If the
            user passed in counted data, bin edges must be specified for bins.
          - bin_range: Tuple[float, float], optional. Specifies the binning range to consider for 
            np.histogram(). By default, if not passed, the lowest bin edge and highest bin edge
            default to the min and max of the data respectively.
          - counted: bool, True specifies whether data has already been counted up for each bin, False
            specifies that data is the raw data that still needs to be binned. Defaults to False.
          - weights: npt.ArrayLike, optional. Ensure same length as data. If counted = False, weights
            is interpreted as the weight to apply to each corresponding data event. If counted = True 
            and weights were used in the counting process before hand, weights acts as the sum of 
            weights squared per bin. Weights set to 1 if set to None.
          - include_error: bool. Whether to include poissonian calculated error bars for plotting.
            Defaults to False
          - normalize: bool. Normalizes the histogram, default False.
          - hist_type: str, for various types of histogram appearances. Options include "step", 
            "stepfilled", "bar", and "point". Defualts to "stepfilled".
          - err_type: str. Specifies the error type of a histogram if errors are to be plotted. Options
          - alpha: float, sets the opacity of a "filled" or "pattern" histogram. Defaults to 1 for 
            completely solid color. 0 corresponds to transparent.
          - label: name given to histogram to be shown in legend
          - kwargs: various other key-word arguments to matplotlib's ax.hist()
        """
        # perform an initial length check for data and weights (if provided)
        if weights is not None:
            data, weights = check_shape(data, weights, "data", "weights")
            self.weights = weights
        # if no weights are passed, default the weights to be all 1
        else:
            self.weights = np.ones_like(data)

        self.counted = counted

        ############################################################################################
        # Compute the histogram counts, bin edges, and uncertainties
        ############################################################################################
        # organize data if user passed in already counted data
        if counted:
            if type(bins) == int:
                raise ValueError(f"Passed in bins={bins}, which is an int, while setting counted="+
                                 f"{counted}. Ensure an arraylike of binedges is passed.")

            if len(data) != len(bins) - 1:
                raise ValueError(f"Specified counted=True, but length of the data array is not the "+
                                 f"length of the bin edges - 1.")

            self.data = data
            self.bins = bins
            
            # calculate the errors in each bin:
            if include_error:
                # assumes sum of squared weights per bin
                if weights is not None:
                    self.err = np.sqrt(weights)
                else:
                    self.err = np.square(data)
            else:
                self.err = None
        
        # if the user passed in raw, uncounted data
        else:
            if bin_range is not None:
                self.data, self.bins = np.histogram(data, bins=bins, range=bin_range, weights=weights)
            else:
                self.data, self.bins = np.histogram(data, bins=bins, weights=weights)

            # calculate the errors on each bin
            if include_error:
                # compute err as sqrt of sum of weights squared per bin
                if weights is not None:
                    self.err = np.sqrt(np.histogram(data, bins=bins, weights=weights**2)[0])
                else:
                    self.err = np.sqrt(self.data)
            else:
                self.err = None

        # compute normalization if requested
        if normalize:
            sum_counts = np.sum(self.data) if self.counted else np.sum(self.weights)
            self.data = self.data/sum_counts
            if self.err is not None: self.err = self.err/sum_counts 

        self.normalize = normalize

        ############################################################################################
        # store the appearance attributes and other histogram settings
        ############################################################################################
        # store the appearance attributes
        self.label = label
        self.hist_type = hist_type
        self.err_style = err_style
        self.alpha = alpha
        self.kwargs = kwargs

    def draw(self, ax):
        """
        Draws the histrogram on the supplied axes
        """
        # plot the main histogram contents
        match self.hist_type:
            case "step":
                handle = ax.stairs(self.data, self.bins, alpha=self.alpha, **self.kwargs)

            case "stepfilled":
                handle = ax.stairs(self.data, self.bins, fill=True, alpha=self.alpha, **self.kwargs)

            case "bar":
                bincenters = (self.bins[1:] + self.bins[:-1])/2
                handle = ax.bar(bincenters, self.data, align="center", linewidth=1, alpha=self.alpha, **self.kwargs)

            case "point":
                bincenters = (self.bins[1:] + self.bins[:-1])/2
                handle = ax.plot(bincenters, self.data, ms=1.5, mc="black", **self.kwargs)

            case _:
                raise ValueError(f"{self.hist_type} is an invalid histogram type. Choose either "+
                                 "'step', 'stepfilled', or 'bar'.")

        # plot the error bars if requested. can plot in 3 different styles
        if self.err is not None:
            bin_edges = self.bins
            match self.err_style:
                # ATLAS style: black diagonal bars
                case "ATLAS":
                    verts = []

                    # Upper edge
                    for i in range(len(bin_edges)-1):
                        binl = bin_edges[i]; binr = bin_edges[i+1]
                        y = self.data[i]
                        e = self.err[i]
                        verts.append((binl, y + e))
                        verts.append((binr, y + e))

                    # Lower edge (reversed)
                    for i in range(len(bin_edges)-1, 0, -1):
                        binl = bin_edges[i-1]; binr = bin_edges[i]
                        y = self.data[i-1]
                        e = self.err[i-1]
                        verts.append((binr, y - e))
                        verts.append((binl, y - e))

                    # Create polygon with hatching
                    poly = Polygon(verts, closed=True, facecolor='none', edgecolor='black', 
                                   hatch='///////////', hatch_linewidth=0.5, linewidth=0)
                    ax.add_patch(poly)

                # faint +/- band of the same color around histogram bins
                case "fillbetween":
                    # compute the low and high limits for the band
                    low = self.data - self.err; high = self.data + self.err

                    # duplicate last value of histogram counts for fill_between
                    low = np.append(low, low[-1]); high = np.append(high, high[-1])

                    ax.fill_between(self.bins, high, low, step="post", color=handle.get_edgecolor(),
                                    alpha=0.35, linewidth=0.3)

                # error bars about each bin
                case "errorbar":
                    bincenters = (bin_edges[1:] + bin_edges[:-1]) / 2

                    # obtain a good color for the error bars
                    match self.hist_type:
                        case "bar" | "stepfilled":
                            errorbar_color = "black"
                        case "step" | "point":
                            errorbar_color = handle.get_facecolor()

                    hist_errbar = ErrorBar(bincenters, self.data, self.err, linestyle='none', 
                                           color=errorbar_color)
                    hist_errbar.draw(ax)

                case _:
                    print(f"Warning: {self.err_style} not a error style.")
                    print("Valid error types are ['ATLAS', 'fillbetween', 'errorbar'].")


        return handle


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
