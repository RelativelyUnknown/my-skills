# Source

- Upstream: https://github.com/wshobson/agents
- Path: `plugins/python-development/skills/python-observability/`
- Commit: 4bde3168b43c0655c4d00ea2726e631719908a6d
- Licence: MIT, Copyright (c) 2024 Seth Hobson. The upstream `LICENSE` is kept next to this file and applies to the adapted material.
- Adapted: 7 November 2026.

## What changed

- The upstream body (229 lines) and details (186 lines) are condensed to about 20 rules and one examples file. Rewritten around the standard library first (the upstream quick start is structlog) and OpenTelemetry's API/SDK split; structlog, the FastAPI middleware listing and the generic "golden signals" tutorial are dropped. Semantic log levels and bounded cardinality are kept.
- Run on Python 3.13 with prometheus-client 0.26.0 and OpenTelemetry 1.45.2 (installed in a scratch environment, not a dependency of this repository): a context variable reaches log records across `await`, `gather` and `to_thread`; `extra={"message": ...}` raises `KeyError`; lazy log arguments are not formatted when the level is off; Prometheus adds `_total` to counters and every label combination is a series; OpenTelemetry spans are non-recording before the SDK is configured, tasks started by `gather` become children of the current span, and `record_exception` adds an `exception` event.
- From the Prometheus client and OpenTelemetry documentation, not run: multiprocess mode, the `OTEL_*` environment variables, `opentelemetry-instrument`, and header propagation.
