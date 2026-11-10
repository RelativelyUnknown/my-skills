# Logging

A log line is for the person debugging at 3 a.m. who has only the log. Ask: what would they need to see, once, in the right place? Not the same fact twice, not a secret, not noise that buries the line that matters.

- Log or raise, never both. `logger = logging.getLogger(__name__)` per module; lazy formatting: `logger.info("loaded %s rows", n)`. Never log secrets, tokens or full request bodies.
- Log a caught error with `logger.exception`, not `logger.error(str(e))`.
- A library never configures handlers or calls `basicConfig`: see `library/shared/api-design.md`.
