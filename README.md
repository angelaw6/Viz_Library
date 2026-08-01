# prettyplots

A tiny [matplotlib](https://matplotlib.org/) wrapper that makes soft, pretty,
pastel plots — a **pink · white · yellow · green** palette, black lines,
gradient bars, a faint pink-blob background and frosted-glass panels.

- **Minimal deps:** just matplotlib (and numpy, which ships with it).
- **Tiny:** the whole library is one file, under 200 lines.

## Install

Straight from GitHub (installs it like any library):

```bash
pip install "git+https://github.com/angelaw6/Viz_Library.git"
```

Or clone and install in editable/development mode:

```bash
git clone https://github.com/angelaw6/Viz_Library.git
cd Viz_Library
pip install -e ".[dev]"        # editable install + dev tools (pytest, ruff)
```

Then, in any Python session:

```python
import prettyplots as pp
```

## Quickstart

```python
import prettyplots as pp

pp.set_theme()

# single plot
fig, ax = pp.bar(["lily", "rose", "iris"], [5, 3, 6], title="Bloom")
fig.savefig("bar.png")

# a grid — background + frosted panels applied automatically
fig, axes = pp.subplots(2, 2)
pp.bar(["a", "b", "c"], [3, 5, 2], ax=axes[0, 0])
pp.line([0, 1, 2, 3], [1, 3, 2, 4], ax=axes[0, 1])
pp.scatter([1, 2, 3], [2, 1, 3], ax=axes[1, 0])
pp.pie([4, 3, 2], labels=["a", "b", "c"], ax=axes[1, 1])
```

Or run the showcase:

```bash
python examples/quickstart.py   # writes examples/showcase.png
```

## Functions — a quick walkthrough

Every plotting function returns `(fig, ax)`, so you can keep customizing with
plain matplotlib afterward. Pass `ax=` (e.g. an axis from `pp.subplots`) to draw
into a grid; leave it out and the function makes its own figure — background and
frosted panel included.

### `set_theme(font_scale=1.0)`
Applies the whole aesthetic globally through matplotlib's settings: the
pink/white/yellow/green color cycle, black axes and text, and bold, enlarged
titles and labels. **Call it once at the top of your script.** `font_scale`
scales every font size up or down.

### `subplots(nrows=1, ncols=1, **kw)`
Drop-in replacement for `plt.subplots`. It builds the grid, paints the soft
pink-blob **background** behind the whole figure, and turns each cell into a
translucent **frosted panel** with a small floral motif. Extra keywords (e.g.
`figsize=`) pass straight through. Returns `(fig, axes)`.

### `bar(categories, values, gradient=True, title=…, xlabel=…, ylabel=…, ax=None)`
Bar chart where bars cycle through the pastel palette and get a crisp black
outline. `gradient=True` gives each bar a soft top-to-bottom fade; set
`gradient=False` for flat solid bars.

### `line(x, y, fill=True, label=…, title=…, xlabel=…, ylabel=…, ax=None)`
Line chart drawn with a bold **black** stroke (readable over the frosted panel).
`fill=True` adds a soft blush fill under the curve; pass a `label` to get a
legend.

### `scatter(x, y, color=BLOSSOM, label=…, title=…, xlabel=…, ylabel=…, ax=None)`
Scatter plot with pastel points and black outlines. `color` sets the fill
(defaults to the signature blossom pink).

### `hist(data, bins=10, color=BLOSSOM, title=…, xlabel=…, ylabel=…, ax=None)`
Histogram with a single pastel fill and black outline. `bins` controls the
number of buckets.

### `pie(values, labels=None, title=…, ax=None)`
Pie chart with pastel wedges, black outlines, and percentage labels. Sits
directly on the background (no frosted panel) so the circle reads cleanly.

### `background(fig=None)`
Paints just the pink-blob background on a figure (defaults to the current one).
Useful if you build a figure by hand and want the backdrop without `subplots`.

### `FILLS`
The palette itself — a list of hex colors (`pp.FILLS`) if you want to use the
theme's colors directly in your own matplotlib code.

## Customizing

- **Colors:** edit `FILLS` / the palette constants at the top of
  `src/prettyplots/__init__.py`.
- **Background:** tweak the `spots` list in `_blobs()`.
- **Frosting:** change the panel alpha in `_frost()`.

## Running tests

```bash
pytest
```

## License

MIT — see [LICENSE](LICENSE).
