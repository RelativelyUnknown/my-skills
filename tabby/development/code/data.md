# Data and model code

Data code rarely raises; it returns plausible wrong numbers. So check the data at every step while you build, and keep a few assertions at the load boundary: `df.shape`, `df.dtypes`, `df.isna().sum()`, a unique key, a value range, and a small hand-computed example whose answer you know.

## Loading

- State the types instead of letting inference decide: `dtype=` or a schema, `parse_dates`, `usecols`, `encoding`. Inference turns IDs with leading zeros into numbers, integer columns with a missing value into floats, and mixed columns into `object`.
- A file that does not fit in memory is read lazily or in chunks (`polars.scan_*`, pyarrow datasets, pandas `chunksize`), not loaded whole. Store intermediate data as Parquet, not CSV or pickle (`pickle` also runs code on load).
- Money is `Decimal` or integer cents, never float. Compare floats with `math.isclose` or `np.isclose`. Timestamps are timezone-aware and stored in UTC; never mix naive and aware.

## Tables

- A join can silently multiply rows when a key is duplicated. Check the row count before and after, and say what you expect: `pandas.merge(..., validate="many_to_one")`, `polars` `join(..., validate="m:1")`.
- Nulls: `NaN != NaN`; a group-by drops null keys unless told otherwise (`dropna=False` in pandas); `fillna(0)` turns "unknown" into "zero"; sums and means of empty groups differ between libraries. Decide what a missing value means before filling it.
- Do not loop over rows (`iterrows`, `apply(axis=1)`) for work a vectorised or expression operation does; the loop is 10 to 1000 times slower. Measure before you tune ([performance](../performance/index.md)).
- pandas: assign with `.loc` (chained assignment may write to a copy), remember that assigning a Series aligns on the index, and check `pd.__version__` before relying on copy-on-write behaviour. In polars prefer expressions over `map_elements`, which runs Python per row.

## Models

- Split first, then fit anything. Scalers, imputers, encoders, target encoding, PCA and feature selection learn from data, so they are fitted on the training part only. Put them in a `Pipeline` or `ColumnTransformer` so that cross-validation refits them in each fold.
- Pick the split by how the model is used: time-ordered data splits by time (`TimeSeriesSplit`, no shuffling); rows from the same user, patient or machine split by group (`GroupKFold`); duplicate rows must not sit on both sides.
- Leakage looks like a score that is too good. Ask of each feature: would it be known at prediction time? A column computed from the label, from later rows or from a rolling window that includes the target row leaks it.
- Report a baseline next to the score (the mean, the majority class, last week's value). For imbalanced classes report precision, recall or PR-AUC, not accuracy. Do not tune against the test set more than once.
- Fix the seeds (`random_state=`, `np.random.default_rng(seed)`), and save the model together with its preprocessing and the library versions.

## Notebooks

Keep the logic in a module with tests and call it from the notebook. A notebook must run top to bottom after a restart. Do not convert a project's notebooks to scripts, or strip their outputs, unasked.
