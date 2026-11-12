#!/usr/bin/env bash
# Builds the fixture for the `ml-leaky-validation` case.
set -euo pipefail
mkdir -p "$(dirname pyproject.toml)"
cat > pyproject.toml <<'__FIXTURE_EOF__'
[project]
name = "demand"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["pandas", "scikit-learn"]
__FIXTURE_EOF__
mkdir -p "$(dirname train.py)"
cat > train.py <<'__FIXTURE_EOF__'
"""Train the weekly demand model. data/sales.csv has columns store_id, week_start (date), price, promo, units."""
import pandas as pd
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("data/sales.csv", parse_dates=["week_start"])
df["avg_units_store"] = df.groupby("store_id")["units"].transform("mean")
features = ["price", "promo", "avg_units_store"]
X = StandardScaler().fit_transform(df[features])
y = df["units"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
model = GradientBoostingRegressor(random_state=0).fit(X_train, y_train)
print("R2", r2_score(y_test, model.predict(X_test)))
__FIXTURE_EOF__
git init -q -b main
git add -A
git -c user.email=eval@example.com -c user.name=eval commit -qm base
