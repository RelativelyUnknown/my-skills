# Logging and security

For a library's logging setup (`NullHandler`, no `basicConfig`), see the library bundle, if installed.

- Log or raise, never both. `logger = logging.getLogger(__name__)` per module; lazy formatting: `logger.info("loaded %s rows", n)`. Never log secrets, tokens or full request bodies.
- No secrets in code, tests or fixtures; read them from the environment. Parameterized SQL only. No `shell=True` with interpolated values. No `eval`, `exec`, `pickle` or `yaml.load` on untrusted data.
