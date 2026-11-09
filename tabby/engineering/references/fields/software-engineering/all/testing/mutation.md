# Mutation testing

Coverage shows which lines ran; mutation testing shows which behavior the tests would notice. Run it periodically (before a release, or weekly), not on every commit.

```bash
uv add --dev mutmut
# pyproject.toml
# [tool.mutmut]
# source_paths = ["src/"]
# pytest_add_cli_args_test_selection = ["tests/"]
uv run mutmut run
uv run mutmut browse        # surviving mutants; press r to retest after strengthening a test
```

- Add `mutants/` to `.gitignore`. mutmut needs `fork`, so on Windows run it in WSL.
- A surviving mutant means a missing or weak test. Strengthen the test. Never change the code to kill a mutant.
- Without a mutation tool, do the manual version for any new test: break the function on purpose, confirm the test fails, restore it.
