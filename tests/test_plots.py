"""Basic smoke tests for prettyplots."""

import matplotlib

matplotlib.use("Agg")  # non-interactive backend for tests

import prettyplots as pp


def test_set_theme_runs():
    pp.set_theme()
    pp.set_theme(palette="vibrant", font_scale=1.2)


def test_get_palette():
    colors = pp.get_palette("default")
    assert isinstance(colors, list)
    assert all(c.startswith("#") for c in colors)


def test_line_returns_fig_ax():
    fig, ax = pp.line([1, 2, 3], [4, 5, 6], title="t", label="a")
    assert fig is not None
    assert ax.get_title() == "t"


def test_scatter_returns_fig_ax():
    fig, ax = pp.scatter([1, 2, 3], [4, 5, 6])
    assert ax.collections  # a PathCollection was added


def test_bar_returns_fig_ax():
    fig, ax = pp.bar(["a", "b"], [1, 2])
    assert ax.patches  # bars were drawn
