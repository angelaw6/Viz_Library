"""Basic smoke tests for prettyplots."""

import matplotlib

matplotlib.use("Agg")  # non-interactive backend for tests

import matplotlib.pyplot as plt

import prettyplots as pp


def test_set_theme_runs():
    pp.set_theme()
    pp.set_theme(font_scale=1.2, background=False)


def test_get_palette():
    colors = pp.get_palette()
    assert isinstance(colors, list)
    assert all(c.startswith("#") for c in colors)


def test_line_returns_fig_ax():
    fig, ax = pp.line([1, 2, 3], [4, 5, 6], title="t", label="a")
    assert ax.get_title() == "t"


def test_scatter_returns_fig_ax():
    fig, ax = pp.scatter([1, 2, 3], [4, 5, 6])
    assert ax.collections


def test_bar_with_pattern():
    fig, ax = pp.bar(["a", "b"], [1, 2], pattern="dots")
    assert ax.patches


def test_hist_and_pie():
    fig, ax = pp.hist([1, 1, 2, 3, 3, 3], bins=3)
    assert ax.patches
    fig2, ax2 = pp.pie([1, 2, 3], labels=["x", "y", "z"])
    assert ax2.patches


def test_prettify_recolors_patches():
    fig, ax = plt.subplots()
    ax.bar(["a", "b", "c"], [1, 2, 3])  # plain matplotlib
    pp.prettify(ax, pattern="stars")
    assert ax.patches[0].get_facecolor()[:3] != (0, 0, 0)


def test_sprinkles():
    fig, ax = pp.line([1, 2], [1, 2])
    pp.sprinkles(ax, glyph="♥")
    assert len(ax.texts) >= 1
