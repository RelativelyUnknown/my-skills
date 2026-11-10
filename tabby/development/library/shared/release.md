# Release

## Never without being asked

"Prepare a release" is not "publish". Do not commit, tag, push, upload (`twine upload`, `uv publish`) or run the release workflow unless asked. Never write a token into a file. Changing the public API or removing a deprecated name needs approval.

## Prepare (exact steps)

1. Working tree clean and the full check green (`make check` or the project's equivalent).
2. **One version, one place.** The version lives in `pyproject.toml` (or comes from a VCS tag through the build backend). Code reads it with `importlib.metadata.version("<pkg>")`. If a second literal exists (`__version__ = "0.3.0"`), remove it or derive it from the metadata instead of updating both, and say so in the report.
3. Bump the version. Pick it from the changes: removal or incompatible change is breaking, new feature is minor, fix is patch. For `0.x`, follow the project's existing convention.
4. Changelog: one entry for this version and date, written for users: what they must change (breaking), what is deprecated and its replacement, what was added, what was fixed. Not commit messages.
5. Build and verify:

```bash
uv build                       # sdist + wheel in dist/
uvx twine check dist/*         # metadata renders on PyPI
unzip -l dist/*.whl            # data files, py.typed and every subpackage are present
```

6. Smoke-test the wheel, not the source tree. Install it into a clean environment and call the package from outside the repository; data files missing from the wheel only show up here:

```bash
uv venv /tmp/wheel-env && uv pip install --python /tmp/wheel-env/bin/python dist/*.whl
cd /tmp && /tmp/wheel-env/bin/python -c "import <pkg>; print(<pkg>.__file__)"   # path must be in /tmp/wheel-env
```
7. Report the version, the changelog entry, the commands with their output, and what remains for a person to do (tag, push, publish).

## Publish automatically (trusted publishing)

Use `development/assets/release.yml`. It builds in one job and publishes from another, so only the publish job holds `id-token: write`. There is no API token to leak or rotate.

- A person must register the trusted publisher on PyPI first (owner, repository, workflow file name, environment `pypi`); say so, do not try to do it. Until then the first upload fails.
- Renaming the repository or the workflow file breaks the match. PyPI does not accept a reusable workflow as the trusted workflow. A pending publisher expires after inactivity and does not reserve the package name.
- The build job fails when the tag does not equal `v` plus the package version.
- Pin each action to its latest release tag (`git ls-remote --tags https://github.com/<owner>/<action>`). `pypa/gh-action-pypi-publish` creates attestations by default under trusted publishing.
- Protect the `pypi` environment with required reviewers if the project wants a manual gate.

## Compatibility and deprecation

- Declare `requires-python` (lower bound, no upper bound) and test in CI on the Python target and the newest release.
- Deprecation and extras are [api-design.md](api-design.md) rules: deprecate for at least one minor release before removing, and keep the base install small.

## Fixing a broken wheel

Reproduce with step 6 first. Typical cause: a file outside the package directory read through `__file__`. Move it into the package, load it with `importlib.resources.files("<pkg>")`, rebuild and repeat the check. Do not add paths to `sys.path` or test only an editable install.
