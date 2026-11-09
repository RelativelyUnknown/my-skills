# Docstrings and API reference

Formats from PEP 257, numpydoc and the Google Python Style Guide. What to say and never say: `../../engineering/references/fields/software-engineering/all/code/comments.md`.

## Choosing a format

| Project | Use |
| --- | --- |
| Already has docstrings | Their format, even if you prefer another |
| Scientific, data or numerical library (NumPy, pandas, SciPy, scikit-learn style) | numpydoc |
| Application or general library, short docstrings | Google style |
| Sphinx project with field lists | reST fields (`:param x:`, `:returns:`) |

Never mix formats in one package. Type hints carry types; repeat a type in the docstring only where the convention requires it (numpydoc's validator expects `x : int`).

## PEP 257 basics

- Triple double quotes. One line: `"""Return the user's display name."""`. Multi-line: summary line, blank line, details, closing quotes on their own line.
- Summary: one sentence on one line, ends with a period, does not restate the signature.
- PEP 257 and numpydoc use the imperative ("Return", "Compute"); Google style permits "Returns ...". Keep the project's.
- Class docstring: what an instance represents; constructor parameters there or in `__init__`, not both. Module docstring: one line of purpose. Private helpers get one only when not obvious.

## numpydoc

Section order: summary, extended summary, Parameters, Returns/Yields, Raises, Warns, See Also, Notes, References, Examples. Only sections with content.

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

    Examples
    --------
    >>> resample(prices, "1h").head(2)
    2026-01-01 00:00:00    10.5
    2026-01-01 01:00:00    11.0
    Freq: h, dtype: float64
    """
```

- Headers underlined with dashes of equal length. Parameter lines: `name : type`; optional ones say `default X` or `optional`. Closed sets: `{"a", "b"}`.
- Validate structure with the `numpydoc-validation` pre-commit hook or `numpydoc_validation_checks` in Sphinx.

## Google style

```python
def fetch_rows(table: str, *, limit: int = 100) -> list[Row]:
    """Fetch rows from a table, newest first.

    Args:
        table: Fully qualified table name.
        limit: Maximum number of rows to return.

    Returns:
        The rows, at most ``limit``. Empty if the table is empty.

    Raises:
        TableNotFoundError: If the table does not exist.
    """
```

Sections: `Args:`, `Returns:`/`Yields:`, `Raises:`, `Attributes:` (classes), `Examples:`, `Note:`. No types when annotated.

## Rendering with Sphinx or MkDocs

- Sphinx: `sphinx.ext.autodoc` plus `napoleon` (numpydoc or Google style) or the `numpydoc` extension. MkDocs: `mkdocstrings[python]` with `docstring_style` set to the project's format.
- Cross-reference objects (`:func:`pkg.load`` in reST, `[pkg.load][]` in mkdocstrings), not plain text.
- Build with warnings as errors (`sphinx-build -W`, `mkdocs build --strict`) so broken references fail CI.

## Examples in docstrings

- Doctest format (`>>>`), short, deterministic output. Run them: `pytest --doctest-modules` or `python -m doctest`.
- Avoid varying output (addresses, timestamps); show a stable form or use `# doctest: +ELLIPSIS` on purpose. One example of the common call beats five covering every parameter.

## Lint configuration

```toml
[tool.ruff.lint]
extend-select = ["D2", "D3", "D4"]   # docstring format rules; D1xx (missing docstrings) left off

[tool.ruff.lint.pydocstyle]
convention = "numpy"   # or "google", "pep257"
```

`convention` turns off rules that conflict with that format (D401, imperative summary, is off under `google`). Do not select `D1xx` missing-docstring rules: they push filler onto self-explaining code ([tooling.md](../../engineering/references/fields/software-engineering/library/shared/tooling.md)). Add docstrings where the reader needs them.
