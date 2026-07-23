"""prettyplots: a small library for making pretty plots.

Example
-------
>>> import prettyplots as pp
>>> pp.set_theme()
>>> fig, ax = pp.line([1, 2, 3], [4, 5, 6], title="Hello")
"""

from __future__ import annotations

from .palettes import PALETTES, get_palette
from .plots import bar, line, scatter
from .theme import set_theme

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "set_theme",
    "get_palette",
    "PALETTES",
    "line",
    "scatter",
    "bar",
]
