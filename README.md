# prettyplots

A tiny [matplotlib](https://matplotlib.org/) wrapper that makes soft, pretty,
pastel plots — a **pink · white · yellow · green** palette, black lines,
gradient bars, a faint pink-blob background and frosted-glass panels.

- **Minimal deps:** just matplotlib (and numpy, which ships with it).
- **Tiny:** the whole library is one file, under 200 lines.

## Install (editable / development)

```bash
pip install -e ".[dev]"
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

## API

| Function | What it does |
|---|---|
| `set_theme(font_scale=1.0)` | Apply the theme globally (call once). |
| `subplots(nrows, ncols, **kw)` | `plt.subplots` + blob background + frosted panels. |
| `bar(cats, vals, gradient=True, ...)` | Gradient (or solid) pastel bars. |
| `line(x, y, fill=True, ...)` | Black line with an optional soft fill. |
| `scatter(x, y, color=..., ...)` | Pastel points, black outlines. |
| `hist(data, bins=10, ...)` | Pastel histogram. |
| `pie(values, labels=..., ...)` | Pastel wedges, black outlines. |
| `background(fig=None)` | Draw just the pink-blob background. |

Every plotting function returns `(fig, ax)` so you can keep customizing with
plain matplotlib. Pass `ax=` (e.g. from `pp.subplots`) to draw into a grid.

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
