"""Plotting functions.

Each function is a thin, opinionated wrapper around matplotlib that returns
the ``(fig, ax)`` pair so you can keep customizing. This is the module you'll
most likely grow as you add new chart types.
"""

from __future__ import annotations

from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib.axes import Axes
from matplotlib.figure import Figure


def _prep_ax(ax: Axes | None) -> tuple[Figure, Axes]:
    """Return a ``(fig, ax)`` pair, creating one if ``ax`` is None."""
    if ax is None:
        fig, ax = plt.subplots()
    else:
        fig = ax.figure
    return fig, ax


def _finalize(
    ax: Axes,
    title: str | None,
    xlabel: str | None,
    ylabel: str | None,
    legend: bool,
) -> None:
    """Apply common labeling to an axes."""
    if title:
        ax.set_title(title)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if legend and ax.get_legend_handles_labels()[1]:
        ax.legend()
    ax.figure.tight_layout()


def line(
    x: Sequence[float],
    y: Sequence[float],
    *,
    label: str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ax: Axes | None = None,
    **kwargs,
) -> tuple[Figure, Axes]:
    """Draw a line plot. Extra ``kwargs`` pass through to ``ax.plot``."""
    fig, ax = _prep_ax(ax)
    ax.plot(x, y, label=label, **kwargs)
    _finalize(ax, title, xlabel, ylabel, legend=label is not None)
    return fig, ax


def scatter(
    x: Sequence[float],
    y: Sequence[float],
    *,
    label: str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ax: Axes | None = None,
    **kwargs,
) -> tuple[Figure, Axes]:
    """Draw a scatter plot. Extra ``kwargs`` pass through to ``ax.scatter``."""
    fig, ax = _prep_ax(ax)
    ax.scatter(x, y, label=label, **kwargs)
    _finalize(ax, title, xlabel, ylabel, legend=label is not None)
    return fig, ax


def bar(
    categories: Sequence[str],
    values: Sequence[float],
    *,
    label: str | None = None,
    title: str | None = None,
    xlabel: str | None = None,
    ylabel: str | None = None,
    ax: Axes | None = None,
    **kwargs,
) -> tuple[Figure, Axes]:
    """Draw a bar chart. Extra ``kwargs`` pass through to ``ax.bar``."""
    fig, ax = _prep_ax(ax)
    ax.bar(categories, values, label=label, **kwargs)
    _finalize(ax, title, xlabel, ylabel, legend=label is not None)
    return fig, ax
