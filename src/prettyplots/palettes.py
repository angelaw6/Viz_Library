"""Color palettes for prettyplots.

Add your own palettes to the ``PALETTES`` dict. Each palette is just an
ordered list of hex color strings.
"""

from __future__ import annotations

# A few starter palettes. Feel free to add/replace these.
PALETTES: dict[str, list[str]] = {
    "default": ["#4C72B0", "#DD8452", "#55A868", "#C44E52", "#8172B3", "#937860"],
    "vibrant": ["#EE6677", "#228833", "#4477AA", "#CCBB44", "#66CCEE", "#AA3377"],
    "pastel": ["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF", "#DEBB9B"],
}


def get_palette(name: str = "default") -> list[str]:
    """Return the list of hex colors for a named palette.

    Parameters
    ----------
    name:
        Key into :data:`PALETTES`.

    Raises
    ------
    KeyError
        If ``name`` is not a known palette.
    """
    if name not in PALETTES:
        raise KeyError(f"Unknown palette {name!r}. Available: {sorted(PALETTES)}")
    return list(PALETTES[name])
