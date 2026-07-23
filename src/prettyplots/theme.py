"""Global styling / theme for prettyplots.

Call :func:`set_theme` once before plotting to apply nice defaults via
matplotlib's rcParams. Tweak the values here to change the look of every plot.
"""

from __future__ import annotations

from cycler import cycler

import matplotlib as mpl

from .palettes import get_palette


def set_theme(palette: str = "default", font_scale: float = 1.0) -> None:
    """Apply prettyplots' default styling to matplotlib globally.

    Parameters
    ----------
    palette:
        Name of the color palette to use for the color cycle.
    font_scale:
        Multiplier applied to base font sizes.
    """
    colors = get_palette(palette)

    base = 11 * font_scale
    mpl.rcParams.update(
        {
            # color cycle
            "axes.prop_cycle": cycler(color=colors),
            # figure
            "figure.figsize": (7, 4.5),
            "figure.dpi": 110,
            "figure.facecolor": "white",
            # axes / spines
            "axes.facecolor": "white",
            "axes.edgecolor": "#333333",
            "axes.linewidth": 0.8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.titlesize": base + 3,
            "axes.titleweight": "bold",
            "axes.labelsize": base + 1,
            # grid
            "grid.color": "#DDDDDD",
            "grid.linewidth": 0.8,
            # ticks
            "xtick.labelsize": base,
            "ytick.labelsize": base,
            # lines
            "lines.linewidth": 2.0,
            "lines.markersize": 6,
            # legend
            "legend.fontsize": base,
            "legend.frameon": False,
            # font
            "font.size": base,
        }
    )
