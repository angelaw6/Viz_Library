"""Global cute-but-readable styling. Call set_theme() before plotting."""
from __future__ import annotations

from cycler import cycler
import matplotlib as mpl
from matplotlib import font_manager

from .palettes import EDGE, FILLS, PANEL, PAPER, TEXT

# Cute, rounded, still-readable fonts (not full cursive); first installed wins.
CUTE_FONTS = ["Comic Neue", "Comic Sans MS", "Quicksand", "Comfortaa",
              "Baloo 2", "Chalkboard", "Chalkboard SE", "Delius", "Segoe Print"]


def _font_stack() -> list[str]:
    have = {f.name for f in font_manager.fontManager.ttflist}
    return [f for f in CUTE_FONTS if f in have] + ["DejaVu Sans"]


def set_theme(font_scale: float = 1.0, background: bool = True) -> None:
    """Apply the pastel coquette theme globally via matplotlib rcParams.

    font_scale multiplies all font sizes; background=False uses plain white.
    """
    base = 12 * font_scale
    mpl.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": _font_stack(),
        "axes.prop_cycle": cycler(color=FILLS),
        "figure.figsize": (7, 4.5), "figure.dpi": 110,
        "figure.facecolor": PAPER if background else "white",
        "axes.facecolor": PANEL if background else "white",
        "axes.edgecolor": EDGE, "axes.linewidth": 1.4,
        "axes.spines.top": False, "axes.spines.right": False,
        # bold, larger titles & labels for easy readability
        "axes.titlesize": base + 5, "axes.titleweight": "bold",
        "axes.titlecolor": TEXT,
        "axes.labelsize": base + 2, "axes.labelweight": "bold",
        "axes.labelcolor": TEXT,
        "axes.grid": True, "axes.axisbelow": True,
        "grid.color": "#E8D8DE", "grid.linewidth": 0.9,
        "text.color": TEXT, "xtick.color": TEXT, "ytick.color": TEXT,
        "xtick.labelsize": base, "ytick.labelsize": base,
        "lines.linewidth": 2.6, "lines.markersize": 7,
        "patch.edgecolor": EDGE, "patch.linewidth": 1.4,
        "legend.fontsize": base, "legend.frameon": True,
        "legend.facecolor": PANEL, "legend.edgecolor": EDGE,
    })
