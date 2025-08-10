"""
Script contains a basic plotting example with synthetic data. It is meant to demonstrate making
quick plots with utilizing minimal features.
"""

import numpy as np
from plotternova.plot_classes.basic import BasicPlot

# Set random seed for reproducibility
np.random.seed(42)

# Generate time points
t = np.linspace(0, 10, 200)  # 200 points from 0 to 10 seconds

# True model: damped sine wave
A = 5          # amplitude
gamma = 0.3    # damping factor
omega = 2*np.pi*0.8  # frequency
y_true = A * np.exp(-gamma * t) * np.sin(omega * t) + 20

# Add Gaussian noise
noise_level = 0.5
noise = np.random.normal(0, noise_level, size=t.shape)
y_noisy = y_true + noise

y_linear = 11*t

text_info = [
    {
        "text": r"$\mathrm{V}(t)=11t$",
        "coords": (0.8, 0.74),
        "color": "blue",
        "transform": True
    },
    {
        "text": r"$y=Ae^{-\gamma t} \mathrm{sin}(\omega t) + C$",
        "coords": (6.75, 27),
        "color": "red"
    }
]

# test the plotting
basic_plot = BasicPlot(xlabel="time [s]",
                       ylabel="Voltage [V]", 
                       ylog_on=True,
                       text_info=text_info,
                       legend_settings="default outside",
                       style="publication",
                       grid_style="dash-dot")
basic_plot.add_data(t, y_noisy, "Noisy data", c='red', ls="-", lw=1)
basic_plot.add_data(t, y_linear, "Linear", c="blue", ls="--", lw=1)
basic_plot.plot(export=True, file_name="test_basic.png")

