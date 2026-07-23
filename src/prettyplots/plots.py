"""Pretty plots + tools to transform standard matplotlib plots.

Each function returns (fig, ax). Pastel fills get a dark readable outline;
pass pattern= (see PATTERNS) for a cute texture. Use prettify() to restyle
a plot you already made, and sprinkles() for faint decorative glyphs.
"""
from __future__ import annotations
import matplotlib.pyplot as plt

from .palettes import EDGE, FILLS, PATTERNS

# Faint background glyph positions (axes fraction), kept behind the data.
_SPOTS = [(.1, .85), (.3, .6), (.5, .92), (.72, .5), (.88, .8),
          (.18, .3), (.6, .18), (.9, .35), (.42, .45), (.78, .12)]


def _ax(ax):
    return (ax.figure, ax) if ax is not None else plt.subplots()


def _hatch(p):
    return PATTERNS.get(p, p) if p else None


def _label(ax, title, xlabel, ylabel, legend):
    if title: ax.set_title(title)
    if xlabel: ax.set_xlabel(xlabel)
    if ylabel: ax.set_ylabel(ylabel)
    if legend and ax.get_legend_handles_labels()[1]: ax.legend()
    ax.figure.tight_layout()


def line(x, y, *, label=None, color=None, title=None, xlabel=None,
         ylabel=None, ax=None, **kw):
    """Line plot: pastel line with dark-outlined markers."""
    fig, ax = _ax(ax)
    ax.plot(x, y, color=color or FILLS[0], marker="o", markeredgecolor=EDGE,
            markeredgewidth=1.2, label=label, **kw)
    _label(ax, title, xlabel, ylabel, label is not None)
    return fig, ax


def scatter(x, y, *, color=None, label=None, title=None, xlabel=None,
            ylabel=None, ax=None, **kw):
    """Scatter plot: pastel fills, dark outlines."""
    fig, ax = _ax(ax)
    ax.scatter(x, y, c=color or FILLS[3], edgecolors=EDGE, linewidths=1.2,
               s=90, label=label, **kw)
    _label(ax, title, xlabel, ylabel, label is not None)
    return fig, ax


def bar(categories, values, *, pattern=None, title=None, xlabel=None,
        ylabel=None, ax=None, **kw):
    """Bar chart: each bar cycles through the pastel palette."""
    fig, ax = _ax(ax)
    colors = [FILLS[i % len(FILLS)] for i in range(len(values))]
    ax.bar(categories, values, color=colors, edgecolor=EDGE, linewidth=1.5,
           hatch=_hatch(pattern), **kw)
    _label(ax, title, xlabel, ylabel, False)
    return fig, ax


def hist(data, *, bins=10, color=None, pattern=None, title=None, xlabel=None,
         ylabel=None, ax=None, **kw):
    """Histogram: pastel fill, dark outline."""
    fig, ax = _ax(ax)
    ax.hist(data, bins=bins, color=color or FILLS[0], edgecolor=EDGE,
            linewidth=1.4, hatch=_hatch(pattern), **kw)
    _label(ax, title, xlabel, ylabel, False)
    return fig, ax


def pie(values, *, labels=None, title=None, ax=None, **kw):
    """Pie chart: pastel wedges, dark outlines."""
    fig, ax = _ax(ax)
    colors = [FILLS[i % len(FILLS)] for i in range(len(values))]
    ax.pie(values, labels=labels, colors=colors, autopct="%1.0f%%",
           wedgeprops=dict(edgecolor=EDGE, linewidth=1.5), **kw)
    if title: ax.set_title(title)
    ax.figure.tight_layout()
    return fig, ax


def prettify(ax, *, pattern=None):
    """Transform a standard matplotlib axes: recolor bars/patches with the
    pastel palette + dark outline, and optionally add a cute pattern."""
    hatch = _hatch(pattern)
    for i, patch in enumerate(ax.patches):
        patch.set_facecolor(FILLS[i % len(FILLS)])
        patch.set_edgecolor(EDGE)
        patch.set_linewidth(1.5)
        if hatch: patch.set_hatch(hatch)
    ax.figure.canvas.draw_idle()
    return ax


def sprinkles(ax, glyph="✦", color=None, alpha=0.12, size=18):
    """Scatter faint background glyphs behind the data (zorder=0, low alpha)
    so they stay decorative. Try glyph="♥" for hearts, "☘" for clovers."""
    for fx, fy in _SPOTS:
        ax.text(fx, fy, glyph, transform=ax.transAxes, ha="center",
                va="center", color=color or EDGE, alpha=alpha, fontsize=size,
                zorder=0)
    return ax
