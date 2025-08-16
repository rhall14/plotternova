import numpy as np
from plotternova.plot_classes.hist import HistPlot
from plotternova.plot_objects.standard2d import Hist


# generate random data from both normal and exponential distributions for sample plotting
normal_data = np.random.normal(loc=2, scale=2.5, size=5000)
expo_data = np.random.exponential(scale=3, size=3000)
normal_data2 = np.random.normal(loc=12, scale=4, size=6000)

extra_text = [
    {
        "text": "Testing various\nhist_types and\nerror styles",
        "coords": (0.03,0.84),
        "color": "black",
        "transform": True
    }
]

test_hist = HistPlot(stack=False, ratio=False, xlabel=r"$x$", ylabel="Normalized count",\
                     xlim=(-9, 33), ylim=(1e-4, 0.35), legend_settings="default inside", 
                     ylog_on = True, beautify_ticks=True, title="Test histogram plotting", 
                     style="publication", text_info=extra_text)

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

norm_hist2 = Hist(normal_data2,
                 bins=30,
                 counted=False,
                 normalize=True,
                 include_error=True,
                 hist_type="step",
                 err_style="fillbetween",
                 label=r"Normal 2 $\pm 1 \sigma$",
                 linestyle="--",
                 color="#2C9135",
                 )

expo_hist = Hist(expo_data,
                 bins=40,
                 counted=False,
                 normalize=True,
                 include_error=True,
                 hist_type="step",
                 err_style="ATLAS",
                 label="Exponential",
                 color="#d72b34",
                 err_label="Stat. uncertainty"
                 )

test_hist.add_data(norm_hist, norm_hist2, expo_hist)

test_hist.plot(export=True, file_name="test_hist.png")