"""prettyplots — a tiny matplotlib wrapper for soft, pastel, pretty plots.

Pink · white · yellow · green palette, black lines, gradient bars, a faint
pink-blob background and frosted-glass panels. Depends only on matplotlib
(+ numpy, which ships with it).

>>> import prettyplots as pp
>>> pp.set_theme()
>>> fig, ax = pp.bar(["lily", "rose", "iris"], [5, 3, 6], title="Bloom")
"""
from __future__ import annotations

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from cycler import cycler
from matplotlib.colors import LinearSegmentedColormap, to_rgb

__version__ = "0.2.0"

# palette: pink · white-pink · yellow · green (+ a deeper green), black ink
BLOSSOM, DOLCE, YELLOW, GREEN, WILLOW = "#e6b1c4", "#efd4dd", "#efcf7a", "#bcd8a8", "#9c9f69"
BLACK = "#141414"
FILLS = [BLOSSOM, DOLCE, YELLOW, GREEN, WILLOW]
_MOTIFS = [("❀", GREEN), ("✦", YELLOW), ("☘", "#6a823e"), ("❀", BLOSSOM)]

__all__ = ["set_theme", "background", "subplots", "bar", "line", "scatter",
           "hist", "pie", "FILLS", "__version__"]


def set_theme(font_scale: float = 1.0) -> None:
    """Apply the pretty theme globally. Call once before plotting."""
    b = 12 * font_scale
    mpl.rcParams.update({
        "figure.figsize": (7, 4.5), "figure.dpi": 110, "figure.facecolor": "white",
        "axes.prop_cycle": cycler(color=FILLS),
        "axes.edgecolor": BLACK, "axes.linewidth": 1.5,
        "axes.spines.top": False, "axes.spines.right": False,
        "axes.titlesize": b + 4, "axes.titleweight": "bold", "axes.titlecolor": BLACK,
        "axes.labelsize": b + 1, "axes.labelweight": "bold", "axes.labelcolor": BLACK,
        "text.color": BLACK, "xtick.color": BLACK, "ytick.color": BLACK,
        "xtick.labelsize": b, "ytick.labelsize": b,
        "lines.linewidth": 2.4, "lines.markersize": 7, "font.family": "sans-serif",
    })


def _blobs(w=240, h=150):
    """Render the soft pink-blob background as an image array."""
    yy, xx = np.mgrid[0:h, 0:w] / max(w, h)
    img = np.ones((h, w, 3))
    spots = [(.30, .55, .22, BLOSSOM, .5), (.62, .72, .24, DOLCE, .55),
             (.74, .38, .18, BLOSSOM, .4), (.15, .85, .16, DOLCE, .45),
             (.85, .70, .15, BLOSSOM, .35), (.50, .22, .14, DOLCE, .4),
             (.88, .92, .13, GREEN, .3)]
    for cx, cy, r, c, a in spots:
        g = np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * r ** 2)))[..., None]
        img = img * (1 - a * g) + np.array(to_rgb(c)) * (a * g)
    return np.clip(0.5 * img + 0.5, 0, 1)


def background(fig=None):
    """Draw the pink-blob background behind everything in ``fig``."""
    fig = fig or plt.gcf()
    ax = fig.add_axes((0, 0, 1, 1), zorder=-10)
    ax.imshow(_blobs(), extent=(0, 1, 0, 1), aspect="auto")
    ax.axis("off")
    return fig


def _frost(ax, i=0):
    """Make ``ax`` a translucent frosted panel with one sparse motif."""
    ax.set_facecolor((1, 1, 1, 0.55))
    ax.grid(True, color="#C9BFC2", linewidth=0.7, alpha=0.6)
    ax.set_axisbelow(True)
    g, c = _MOTIFS[i % len(_MOTIFS)]
    ax.text(0.93, 0.9, g, transform=ax.transAxes, ha="center", va="center",
            color=c, alpha=0.4, fontsize=12, zorder=1)


def subplots(nrows=1, ncols=1, **kw):
    """Like ``plt.subplots`` but with the blob background + frosted panels."""
    fig, axes = plt.subplots(nrows, ncols, **kw)
    fig.subplots_adjust(hspace=0.38, wspace=0.28, top=0.9)
    background(fig)
    for i, ax in enumerate(np.atleast_1d(axes).ravel()):
        _frost(ax, i)
    return fig, axes


def _one(ax):
    if ax is not None:
        return ax.figure, ax
    fig, ax = plt.subplots()
    background(fig)
    _frost(ax)
    return fig, ax


def _final(ax, title, xlabel, ylabel, legend):
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if legend and ax.get_legend_handles_labels()[1]:
        ax.legend(facecolor=(1, 1, 1, 0.7), edgecolor=BLACK)
    return ax.figure, ax


def bar(categories, values, *, gradient=True, title=None, xlabel=None, ylabel=None, ax=None):
    """Bar chart with pastel gradient (or solid) bars and black outlines."""
    fig, ax = _one(ax)
    vals = np.asarray(values, float)
    colors = [FILLS[i % len(FILLS)] for i in range(len(vals))]
    if not gradient:
        ax.bar(categories, vals, color=colors, edgecolor=BLACK, linewidth=1.6, zorder=3)
    else:
        bars = ax.bar(categories, vals, color="none", edgecolor=BLACK, linewidth=1.6, zorder=3)
        xlim = ax.get_xlim()
        for b, c in zip(bars, colors):
            cm = LinearSegmentedColormap.from_list("g", [c, np.array(to_rgb(c)) * .5 + .5])
            ax.imshow(np.linspace(0, 1, 256).reshape(-1, 1), cmap=cm, origin="lower",
                      aspect="auto", zorder=2,
                      extent=(b.get_x(), b.get_x() + b.get_width(), 0, b.get_height()))
        ax.set_xlim(xlim)
        ax.set_ylim(0, vals.max() * 1.18)
    return _final(ax, title, xlabel, ylabel, False)


def line(x, y, *, label=None, fill=True, title=None, xlabel=None, ylabel=None, ax=None):
    """Line plot with a black stroke and an optional soft pastel fill."""
    fig, ax = _one(ax)
    if fill:
        ax.fill_between(x, y, color=BLOSSOM, alpha=0.3, zorder=2)
    ax.plot(x, y, color=BLACK, linewidth=2.4, zorder=4, label=label)
    return _final(ax, title, xlabel, ylabel, label is not None)


def scatter(x, y, *, color=BLOSSOM, label=None, title=None, xlabel=None, ylabel=None, ax=None):
    """Scatter plot with pastel fills and black outlines."""
    fig, ax = _one(ax)
    ax.scatter(x, y, c=color, edgecolors=BLACK, linewidths=1.1, s=90, zorder=3, label=label)
    return _final(ax, title, xlabel, ylabel, label is not None)


def hist(data, *, bins=10, color=BLOSSOM, title=None, xlabel=None, ylabel=None, ax=None):
    """Histogram with a pastel fill and black outline."""
    fig, ax = _one(ax)
    ax.hist(data, bins=bins, color=color, edgecolor=BLACK, linewidth=1.4, zorder=3)
    return _final(ax, title, xlabel, ylabel, False)


def pie(values, *, labels=None, title=None, ax=None):
    """Pie chart with pastel wedges and black outlines (no frosted panel)."""
    fig, ax = _one(ax)
    ax.set_facecolor((1, 1, 1, 0))
    ax.grid(False)
    colors = [FILLS[i % len(FILLS)] for i in range(len(values))]
    ax.pie(values, labels=labels, colors=colors, autopct="%1.0f%%",
           textprops=dict(color=BLACK, fontsize=9),
           wedgeprops=dict(edgecolor=BLACK, linewidth=1.5))
    if title:
        ax.set_title(title)
    return fig, ax
