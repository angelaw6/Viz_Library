"""prettyplots: turn standard matplotlib plots into cute, pastel, readable ones.

>>> import prettyplots as pp
>>> pp.set_theme()
>>> fig, ax = pp.bar(["a", "b", "c"], [3, 5, 2], title="Cute!", pattern="dots")
>>> pp.sprinkles(ax, glyph="♥")
"""
from __future__ import annotations

from .palettes import EDGE, FILLS, PATTERNS, get_palette
from .plots import bar, hist, line, pie, prettify, scatter, sprinkles
from .theme import set_theme

__version__ = "0.1.0"
__all__ = ["__version__", "set_theme", "get_palette", "FILLS", "EDGE",
           "PATTERNS", "line", "scatter", "bar", "hist", "pie", "prettify",
           "sprinkles"]
