"""Quickstart example for prettyplots.

Run with:  python examples/quickstart.py
Saves a PNG next to this file.
"""

import numpy as np

import prettyplots as pp

pp.set_theme(palette="vibrant")

x = np.linspace(0, 2 * np.pi, 100)
fig, ax = pp.line(x, np.sin(x), label="sin", title="Pretty line plot", xlabel="x", ylabel="y")
pp.line(x, np.cos(x), label="cos", ax=ax)

fig.savefig("examples/quickstart.png", dpi=150)
print("Saved examples/quickstart.png")
