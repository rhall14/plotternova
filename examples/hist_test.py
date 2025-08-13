import numpy as np
from plotternova.plot_classes.hist import HistPlot
from plotternova.plot_objects.standard2d import Hist


# generate random data from both normal and exponential distributions for sample plotting
normal_data = np.random.normal(loc=2, scale=2.5, size=5000)
expo_data = np.random.exponential(scale=3, size=3000)
expo_err = np.sqrt(expo_data)




test_hist = HistPlot(normalize=False, stack=False, ratio=False, xlabel=r"$x$", ylabel="Frequency",
                     legend_settings="default inside", ylog_on = True, beautify_ticks=True)

test_hist.add_data(Hist(normal_data, bins=30, hist_type="stepfilled", color="#554CE0", label="Normal"),
                   Hist(expo_data, bins=30, hist_type="step", err=expo_err, linestyle="-.", color="#9E2E2E", label="Exponential"))

test_hist.plot(export=True, file_name="test_hist.png")