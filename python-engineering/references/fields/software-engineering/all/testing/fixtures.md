# Fixtures

- Smallest scope that works: the default `function` scope. Widen to `module` or `session` only for something expensive and read-only.
- Shared fixtures live in the `conftest.py` nearest to their users. A fixture used by one file stays in that file.
- Yield for cleanup:

```python
@pytest.fixture
def db(tmp_path):
    conn = connect(tmp_path / "test.db")
    yield conn
    conn.close()
```

- Factory fixtures build variations without one fixture per case:

```python
@pytest.fixture
def make_user():
    def make(name="ada", *, admin=False):
        return User(name=name, admin=admin)
    return make
```

- No `autouse=True` fixture that changes behavior the test does not mention. Autouse is acceptable for isolation only (for example, clearing an environment variable).
- Parametrize inputs, not setup: if every case needs different setup, they are different tests.
- A fixture that returns a value the test never uses should be `@pytest.mark.usefixtures("name")`.
