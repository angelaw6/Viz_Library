"""Coquette / neapolitan pastel palette + a single dark, readable outline.

Colors: warm & cool pinks, lilac purple, four-leaf-clover greens, pastel
blue, cream, chocolate brown. Tweak freely.
"""
from __future__ import annotations

FILLS = [
    "#F4C2D7",  # warm pastel pink
    "#C9A9E9",  # lilac purple
    "#A3D9A5",  # four-leaf-clover green
    "#A7C7E7",  # pastel blue
    "#F6E7CB",  # cream
    "#C89F94",  # chocolate-milk brown
    "#EBB7CE",  # cool rose pink
    "#B7E4C7",  # mint clover
]
EDGE = "#5C4033"   # dark chocolate outline — readable on every fill
TEXT = "#5A3D4E"   # warm dark mauve for titles & labels
PAPER = "#FBF3F0"  # soft cream-pink page background
PANEL = "#FFFBF7"  # near-white plot background (keeps data crisp)

# Native matplotlib hatches that read as cute textures.
PATTERNS = {"dots": "..", "circles": "oo", "sparkles": "**",
            "stars": "*", "swirls": "//", "grid": "xx"}


def get_palette() -> list[str]:
    """Return a copy of the pastel fill colors."""
    return list(FILLS)
