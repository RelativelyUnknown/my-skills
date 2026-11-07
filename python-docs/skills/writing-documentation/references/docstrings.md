# Docstrings and API reference

Formats from PEP 257, the numpydoc standard and the Google Python Style Guide. Content rules (what to say, what never to say) are in `writing-python-code`.

## Contents

- Choosing a format
- PEP 257 basics
- numpydoc
- Google style
- Rendering with Sphinx or MkDocs
- Examples in docstrings
- Lint configuration

## Choosing a format

| Project | Use |
| --- | --- |
| Already has docstrings | Their format, even if you prefer another |
| Scientific, data or numerical library (NumPy, pandas, SciPy, scikit-learn style) | numpydoc |
| Application or general library, short docstrings | Google style |
| Sphinx project with existing field lists | reST fields (`:param x:`, `:returns:`, `:raises ValueError:`) |

Never mix formats in one package. Type hints carry types; do not repeat a type in the docstring unless the convention requires it (numpydoc lists types; with full annotations, a short form like `x : int` is still expected by numpydoc's validator).

## PEP 257 basics

- Triple double quotes. One-line docstring: `"""Return the user's display name."""` on one line, closing quotes on the same line.
- Multi-line: summary line, blank line, then details; closing quotes on their own line.
- Summary line: one sentence that fits on one line, ends with a period, and does not restate the signature ("`parse(text)`: parse text").
- PEP 257 and numpydoc write the summary in the imperative: "Return", "Compute", "Raise", not "Returns". Google style permits the descriptive form ("Returns ..."); keep whichever the project uses.
- Class docstring: what an instance represents; document constructor parameters there (or in `__init__`, per the convention), not both.
- Module docstring: one line of purpose, optionally a short overview listing the main public names.
- Private helpers (`_name`) get a docstring only when the behavior is not obvious.

## numpydoc

Section order: summary, extended summary, Parameters, Returns (or Yields), Receives, Other Parameters, Raises, Warns, Warnings, See Also, Notes, References, Examples. Include only sections with content.

```python
def resample(series, rule, *, closed="left"):
    """Resample a time series to a new frequency.

    Parameters
    ----------
    series : pandas.Series
        Values indexed by a monotonic ``DatetimeIndex``.
    rule : str
        Target frequency as an offset alias, for example ``"15min"``.
    closed : {"left", "right"}, default "left"
        Which side of each bin interval is closed.

    Returns
    -------
    pandas.Series
        The resampled series, one value per bin.

    Raises
    ------
    ValueError
        If the index is not monotonic.

    See Also
    --------
    pandas.Series.resample : The underlying method.

    Examples
    --------
    >>> resample(prices, "1h").head(2)
    2026-01-01 00:00:00    10.5
    2026-01-01 01:00:00    11.0
    Freq: h, dtype: float64
    """
```

- Section headers are underlined with dashes of the same length.
- Parameter lines: `name : type`; optional ones say `default X` or `optional`.
- Closed sets of values: `{"a", "b"}`.
- numpydoc's validator checks structure: the `numpydoc-validation` pre-commit hook, or `numpydoc_validation_checks` in Sphinx.

## Google style

```python
def fetch_rows(table: str, *, limit: int = 100) -> list[Row]:
    """Fetch rows from a table, newest first.

    Args:
        table: Fully qualified table name, for example ``main.sales.orders``.
        limit: Maximum number of rows to return.

    Returns:
        The rows, at most ``limit`` of them. Empty if the table is empty.

    Raises:
        TableNotFoundError: If the table does not exist.
    """
```

Sections: `Args:`, `Returns:` (or `Yields:`), `Raises:`, `Attributes:` (classes), `Example:`/`Examples:`, `Note:`. Indent descriptions under the name; no types when annotated.

## Rendering with Sphinx or MkDocs

- Sphinx: `sphinx.ext.autodoc` plus `sphinx.ext.napoleon` for numpydoc or Google style, or the `numpydoc` extension. `sphinx-autodoc-typehints` moves annotations into the rendered docs.
- MkDocs (Material): `mkdocstrings[python]` with `docstring_style: google | numpy | sphinx` set to the project's format.
- Cross-reference other objects (`:func:`pkg.load`` in reST, `[pkg.load][]` in mkdocstrings) instead of naming them in plain text.
- Build with warnings as errors (`sphinx-build -W`, `mkdocs build --strict`) so broken references fail CI.

## Examples in docstrings

- Doctest format (`>>>`), short, deterministic output. Run them: `pytest --doctest-modules` or `python -m doctest`.
- Avoid output that varies (memory addresses, dict order across versions, timestamps); show a stable representation or use `# doctest: +ELLIPSIS` deliberately.
- One example that shows the common call beats five that show every parameter.

## Lint configuration

```toml
[tool.ruff.lint]
extend-select = ["D2", "D3", "D4"]   # docstring format rules; D1xx (missing docstrings) left off

[tool.ruff.lint.pydocstyle]
convention = "numpy"   # or "google", "pep257"
```

`convention` turns off the rules that conflict with that format; for example, D401 (imperative summary) applies under `numpy` and `pep257` and is off under `google`. Do not select the `D1xx` missing-docstring rules: they push filler docstrings onto code that explains itself (`setting-up-python-packages` says the same). Add docstrings where the reader needs them.
