import numpy as np


# every plot objets must have a draw method supplied with axes to be plotted on

class PointsLines:
    def __init__(self, xdata, ydata, label, **kwargs) -> None:
        """
        Create points and/or lines plot objects that represent data.
        """
        self.xdata = xdata; self.ydata = ydata
        self.label = label

        # store **kwargs for plotting
        self.kwargs = kwargs

    def draw(self, ax):
        handle, = ax.plot(self.xdata, self.ydata, **self.kwargs)
        return handle


class FillBetween:
    pass


class Hist:
    pass


class Matrix:
    pass


class HeatMap:
    pass