"""Basic smoke tests for prettyplots."""

import matplotlib

matplotlib.use("Agg")  # non-interactive backend for tests

import prettyplots as pp


def test_set_theme_runs():
    pp.set_theme()
    pp.set_theme(font_scale=1.2)


def test_subplots_has_background():
    fig, axes = pp.subplots(2, 2)
    # background axes added at zorder -10 in addition to the 4 subplots
    assert len(fig.axes) == 5


def test_bar_gradient_and_solid():
    fig, ax = pp.bar(["a", "b", "c"], [3, 5, 2], title="t")
    assert ax.get_title() == "t"
    fig2, ax2 = pp.bar(["a", "b"], [1, 2], gradient=False)
    assert ax2.patches


def test_line_and_fill():
    fig, ax = pp.line([0, 1, 2], [1, 3, 2], label="a")
    assert ax.get_lines()


def test_scatter():
    fig, ax = pp.scatter([1, 2, 3], [4, 5, 6])
    assert ax.collections


def test_hist():
    fig, ax = pp.hist([1, 1, 2, 3, 3, 3], bins=3)
    assert ax.patches


def test_pie():
    fig, ax = pp.pie([4, 3, 2], labels=["x", "y", "z"])
    assert ax.patches


def test_shared_ax_from_subplots():
    fig, axes = pp.subplots(1, 2)
    pp.bar(["a", "b"], [1, 2], ax=axes[0])
    pp.scatter([1, 2], [3, 4], ax=axes[1])
    assert axes[0].patches and axes[1].collections
