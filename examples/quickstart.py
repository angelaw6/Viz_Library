"""Quickstart example for prettyplots.

Run with:  python examples/quickstart.py
Saves PNGs next to this file.
"""

import numpy as np

import prettyplots as pp

pp.set_theme()

# 1) A cute line plot with background sparkles.
x = np.linspace(0, 2 * np.pi, 120)
fig, ax = pp.line(x, np.sin(x), label="sin", title="Pretty line plot",
                  xlabel="x", ylabel="y")
pp.line(x, np.cos(x), label="cos", color=pp.FILLS[1], ax=ax)
pp.sprinkles(ax, glyph="✦")
fig.savefig("examples/line.png", dpi=150)

# 2) A bar chart with a dotted texture.
fig, ax = pp.bar(["clover", "lilac", "rose", "cream"], [5, 3, 6, 4],
                 title="Pastel bars", ylabel="count", pattern="dots")
fig.savefig("examples/bars.png", dpi=150)

# 3) Transform a *standard* matplotlib plot with prettify().
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.bar(["a", "b", "c"], [2, 5, 3])          # plain matplotlib
ax.set_title("Prettified")
pp.prettify(ax, pattern="stars")            # <- one call restyles it
fig.savefig("examples/prettified.png", dpi=150)

print("Saved examples/line.png, bars.png, prettified.png")
