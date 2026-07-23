# prettyplots

A small Python library for making pretty plots, built on top of
[matplotlib](https://matplotlib.org/).

> Status: early scaffold — the bare-bones structure is in place and ready for
> you to build on.

## Install (editable / development)

```bash
pip install -e ".[dev]"
```

## Quickstart

```python
import prettyplots as pp

pp.set_theme(palette="vibrant")

fig, ax = pp.line([1, 2, 3, 4], [10, 8, 12, 9], title="My first plot",
                  xlabel="x", ylabel="y", label="series A")
fig.savefig("plot.png")
```

Or run the example:

```bash
python examples/quickstart.py
```

## Project layout

```
src/prettyplots/
    __init__.py     # public API
    theme.py        # global styling via set_theme()
    palettes.py     # named color palettes
    plots.py        # plotting functions (line, scatter, bar, ...)
tests/              # pytest smoke tests
examples/           # runnable examples
```

## Where to start coding

- **Add a new chart type:** write a function in `src/prettyplots/plots.py`
  that returns `(fig, ax)`, then export it in `__init__.py`.
- **Change the look:** edit the rcParams in `src/prettyplots/theme.py`.
- **Add colors:** add an entry to `PALETTES` in `src/prettyplots/palettes.py`.

## Running tests

```bash
pytest
```

## License

MIT — see [LICENSE](LICENSE).
