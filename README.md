# PLOTTERNOVA
## About
This is a plotting package designed to take decrease the time spent configuring a nice matplotlib
figure, with simple commmands. There are multpile presets for plot objects, styling, and color
themes that are meant to create nice, potentially paper-quality plots, within a matter of a few
commands. The whole plotternova package is built on plot_classes, which contain specialized figures
and axes for each type of plot. On instances of these plot_classes, you include various different
plot_objects (e.g., lines, points, histograms, etc...) which have nice default appearance options. 
With these plot objects, the user can also pass in other various matplotlib **kwargs that the object 
was built off of. Finally, there are numerous color themes, and styles to choose from for the figure 
and plot objects to get a visually pleasing appearance with minimal effort.

## Setup
Note: If you wish, you can install plotternova in a specific python virtual environment to prevent 
dependency conflicts.

Start by cloning the repository from GitHub onto your desired directory on your local machine, then
navigating to the local repository using
```bash
git clone git@github.com:rhall14/plotternova.git
cd plotternova
```

To create an editable install of the package so you can make your own tweaks to the source code and 
have the changes automatically reflect on your installation of the package, use
```bash
pip install -e .
```
Otherwise, simply run 
```bash
pip install .
```

## Using plotternova
Different plot types are sectioned off into different plot classes in plotternova. For example, to 
make a histogram plot, you must first import the histogram plot class. Then create and instance of 
the histogram plot class, which creates essentially the fig and ax from matplotlib, while applying 
the plot settings passed to it:
```python
from plotternova.plot_classes.hist import HistPlot

test_hist = HistPlot(stack=False, ratio=False, xlabel=r"$x$", ylabel="Normalized count",
                     legend_settings="default inside", ylog_on = True, beautify_ticks=True, 
                     title="Test histogram plotting", style="publication")
```

With an instance of the histogram plot object created, you can add various *plot_objects*, containing 
the data, to the figure. For example, you can add a histogram to the plot by first importing the
plot_object, then creating an instance of it, then adding that object to your figure:
```python
from plotternova.plot_objects.standard2d import Hist

# assumes you have your histogram data from some experiment or simulation
hist_obj = Hist(hist_data, bins=40, counted=False, normalize=True, include_error=True,
                hist_type="stepfilled", err_style="errorbar", label="Normal", color="#554CE0")

test_hist.add_data(hist_obj)
```

Once you have added all of the desired data in the form of plot_objects to your figure, you can call 
the plotting routine by simply running
```python
test_hist.plot(export=True, file_name="test_hist.png")
```
This will create the nicely formatted plot without the headache of setting all of the matplotlib 
settings to do so.

Note that each plot class is specialized to plot certain plot objects, so check the documentation 
for each to know what to plot and what the settings are.

## Styling options
As mentioned before, plotternova comes with many preset styling and color theme options found in the 
`plotternova.theme` package. When instantiating a plot class, you can specify the style and theme, 
like 'presentation' and 'dark theme', which are found in the `plotternova.theme.style` and 
`plotternova.theme.color_theme` modules. Or you can pass in your own style and themes as dictionaries 
for full customization.

plot_objects themselves also come with certain prebuilt appearances, but if you are not satisfied 
with how they look, you can also pass in matplotlib **kwargs to the instantiation of the plot_object 
to fine tune the appearance. 
```python
from plotternova.plot_objects.standard2d import PointsLines

# example creating a line object with various matplotlib kwargs
line1 = PointsLines(xdata, ydata, color="red", ls="-.", marker="x", ms=3)
```
Additionally, you can also choose various color themes for them as well (STILL WORKING ON THIS)