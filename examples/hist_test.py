import numpy as np
from plotternova.plot_classes.hist import HistPlot


# generate random data from both normal and exponential distributions for sample plotting
normal_data = np.random.normal(loc=1.5, scale=0.75, size=5000)
expo_data = np.random.exponential(scale=1, size=5000)




test_hist = HistPlot()