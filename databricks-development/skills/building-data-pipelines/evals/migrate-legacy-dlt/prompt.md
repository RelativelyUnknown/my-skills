---
tags: [building-data-pipelines]
max_turns: 30
timeout_seconds: 900
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
---

Our pipeline file still uses the old DLT API. Update it to the current API without changing behavior.

```python
import dlt
from pyspark.sql.functions import col

@dlt.table
def customers_bronze():
    return spark.readStream.format('cloudFiles').option('cloudFiles.format', 'json').load('/Volumes/main/raw/customers')

@dlt.table
def country_counts():
    return dlt.read('customers_silver').groupBy('country').count()

dlt.create_streaming_table('customers_silver')
dlt.apply_changes(target='customers_silver', source='customers_bronze', keys=['id'], sequence_by=col('ts'), stored_as_scd_type=1)
```

Save it as `pipeline.py`.
