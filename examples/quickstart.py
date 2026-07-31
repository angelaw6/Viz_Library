"""Quickstart for prettyplots — renders a 2x2 showcase.

Run with:  python examples/quickstart.py
"""

import numpy as np

import prettyplots as pp

pp.set_theme()

fig, axes = pp.subplots(2, 2, figsize=(9, 6.2))
cats = ["lily", "rose", "iris", "fern"]

pp.bar(cats, [5, 3, 6, 4], title="Bar", ax=axes[0, 0])

x = np.linspace(-3, 3, 200)
pp.line(x, np.exp(-x**2) + 0.55 * np.exp(-(x - 1.4)**2 * 5) + 0.1,
        title="Line", ax=axes[0, 1])

pp.scatter(np.random.default_rng(11).normal(0, 1, 38),
           np.random.default_rng(3).normal(0, 1, 38), title="Scatter", ax=axes[1, 0])

pp.pie([4, 3, 2, 5], labels=cats, title="Pie", ax=axes[1, 1])

fig.suptitle("prettyplots", fontsize=16, fontweight="bold")
fig.savefig("examples/showcase.png", dpi=150)
print("Saved examples/showcase.png")
