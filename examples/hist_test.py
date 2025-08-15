import numpy as np
from plotternova.plot_classes.hist import HistPlot
from plotternova.plot_objects.standard2d import Hist


# generate random data from both normal and exponential distributions for sample plotting
normal_data = np.random.normal(loc=2, scale=2.5, size=5000)
expo_data = np.random.exponential(scale=3, size=3000)

test_hist = HistPlot(stack=False, ratio=False, xlabel=r"$x$", ylabel="Normalized count",
                     legend_settings="default inside", ylog_on = True, beautify_ticks=True, 
                     title="Test histogram plotting", style="publication")

norm_hist = Hist(normal_data,
                 bins=40,
                 counted=False,
                 normalize=True,
                 include_error=True,
                 hist_type="stepfilled",
                 err_style="errorbar",
                 label="Normal",
                 color="#554CE0"
                 )

expo_hist = Hist(expo_data,
                 bins=40,
                 counted=False,
                 normalize=True,
                 include_error=True,
                 hist_type="step",
                 err_style="ATLAS",
                 label="Exponential",
                 color="#d72b34"
                 )

test_hist.add_data(norm_hist, expo_hist)

test_hist.plot(export=True, file_name="test_hist.png")