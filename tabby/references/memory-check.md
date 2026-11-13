# Check the saved section against the code

Before new work (a feature, a refactor, a release), compare the `## Tabby` section with the code: commits since `reviewed:` (`git rev-list --count <sha>..HEAD`) and whether `pyproject.toml`, `Cargo.toml`, `Makefile` or `.github` changed (`git diff --stat <sha>..HEAD -- ...`). Report the evidence and ask only about changed facts.
