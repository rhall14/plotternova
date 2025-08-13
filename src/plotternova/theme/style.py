# default style to do most quick plotting. No latex render enabled
DEFAULT_STYLE = {
    "figure.figsize": (6, 4),
    "font.family": "serif",
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "axes.titlesize": 14,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "xtick.minor.size": 3,
    "ytick.minor.size": 3,
    "xtick.major.width": 1.1,
    "ytick.major.width": 1.1,
    "xtick.minor.width": 0.75,
    "ytick.minor.width": 0.75,
}

# small figure template for publications
PUB_SMALL_STYLE = {
    "figure.figsize": (4, 3),
    "font.family": "Times New Roman",
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 8,
    "xtick.top": True,
    "ytick.right": True,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 5,
    "ytick.major.size": 5,
    "xtick.minor.size": 3,
    "ytick.minor.size": 3,
    "xtick.major.width": 1,
    "ytick.major.width": 1,
    "xtick.minor.width": 0.75,
    "ytick.minor.width": 0.75,
    "text.usetex": True, # enable LaTeX
    "text.latex.preamble": r"\usepackage{amsmath}"
}

# figure template for publications
PUB_STYLE = {
    "figure.figsize": (6, 4),
    "font.family": "Times New Roman",
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10,
    "xtick.top": True,
    "ytick.right": True,
    "xtick.direction": "in",
    "ytick.direction": "in",
    "xtick.major.size": 6,
    "ytick.major.size": 6,
    "xtick.minor.size": 3,
    "ytick.minor.size": 3,
    "xtick.major.width": 1.25,
    "ytick.major.width": 1.25,
    "xtick.minor.width": 0.8,
    "ytick.minor.width": 0.8,
    # "text.usetex": True, # enable LaTeX
    # "text.latex.preamble": r"\usepackage{amsmath}"
}

# specialized for making larger plots with more celear working
PRESENTATION_STYLE = {
    "figure.figsize": (10, 6),
    "axes.titlesize": 18,
    "axes.labelsize": 16,
    "lines.linewidth": 3,
    "lines.markersize": 8,
}

# ATLAS style figures
ATLAS_STYLE = {

}

# Group them for easy lookup
STYLE_PRESETS = {
    "default": DEFAULT_STYLE,
    "publication small": PUB_SMALL_STYLE,
    "publication": PUB_STYLE,
    "presentation": PRESENTATION_STYLE,
    "ATLAS": ATLAS_STYLE
}

