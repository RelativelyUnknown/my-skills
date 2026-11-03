---
tags: [writing-pyspark-transformations]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Clean up this PySpark function from our silver job, it's slow and the reviewer hated it. Keep the output the same.

```python
from pyspark.sql.functions import *
from pyspark.sql.types import StringType

norm = udf(lambda s: s.strip().upper() if s else None, StringType())

def clean(df, cols):
    for c in cols:
        df = df.withColumn(c, norm(col(c)))
    if df.count() == 0:
        return df
    countries = [r.country for r in df.select('country').distinct().collect()]
    return df.filter(col('country').isin(countries))
```

Write the result to `transforms.py`.
