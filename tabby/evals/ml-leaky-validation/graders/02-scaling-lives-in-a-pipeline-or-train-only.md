---
type: regex
target:
  source: file
  path: "train.py"
pattern: "Pipeline\\(|make_pipeline\\(|ColumnTransformer|\\.fit(_transform)?\\(\\s*X_train"
weight: 3
---

Scaling is fit on the training part only
