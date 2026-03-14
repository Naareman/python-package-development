# 12 — Testing: Mocking

R equivalent: `testthat::local_mocked_bindings()`, `httptest2`, `webfakes`. The goal is
the same: isolate your code from things you don't control.

---

## When to Mock

Mock **external boundaries** — things that are slow, flaky, or have side effects:

- HTTP APIs and web services
- File systems (when testing logic, not I/O)
- Time (`datetime.now()`, `time.time()`)
- Databases and caches
- Environment variables

Do **not** mock:

- Your own package code (test the real thing)
- Standard library basics (don't mock `len()` or `dict.get()`)
- Simple data transformations (just assert the output)

---

## pytest-mock — The Preferred Approach

Use `pytest-mock` over raw `unittest.mock`. It gives you a `mocker` fixture that
auto-cleans up after each test.

```bash
uv add --dev pytest-mock
```

```python
def test_fetch_data_calls_api(mocker):
    mock_get = mocker.patch("my_package.client.httpx.get")
    mock_get.return_value.json.return_value = {"status": "ok"}

    result = fetch_data("https://api.example.com/data")

    mock_get.assert_called_once_with("https://api.example.com/data")
    assert result == {"status": "ok"}
```

### Common mocker methods

```python
mocker.patch("module.path.function")          # replace a function
mocker.patch.object(obj, "method")            # replace a method on an object
mocker.patch.dict("os.environ", {"KEY": "v"}) # patch a dict
mocker.spy(obj, "method")                     # wrap real method, track calls
```

---

## MagicMock Basics

When you need a stand-in object that accepts any attribute or call:

```python
def test_processor_calls_writer(mocker):
    writer = mocker.MagicMock()
    processor = DataProcessor(writer=writer)

    processor.run(records=[{"id": 1}])

    writer.write.assert_called_once()
    assert writer.write.call_args[0][0] == [{"id": 1}]
```

---

## Mocking HTTP Calls

For packages that hit APIs, use `responses` (for `requests`) or `respx` (for `httpx`).

```bash
uv add --dev responses   # if using requests
uv add --dev respx       # if using httpx
```

### With responses

```python
import responses

@responses.activate
def test_fetch_users():
    responses.add(
        responses.GET,
        "https://api.example.com/users",
        json=[{"id": 1, "name": "Alice"}],
        status=200,
    )
    result = fetch_users()
    assert len(result) == 1
    assert result[0]["name"] == "Alice"
```

### With respx

```python
import respx
import httpx

def test_fetch_users(respx_mock):
    respx_mock.get("https://api.example.com/users").mock(
        return_value=httpx.Response(200, json=[{"id": 1, "name": "Alice"}])
    )
    result = fetch_users()
    assert result[0]["name"] == "Alice"
```

---

## monkeypatch — Environment and Attributes

Built into pytest. Best for environment variables and simple attribute swaps.

```python
def test_reads_api_key_from_env(monkeypatch):
    monkeypatch.setenv("API_KEY", "test-key-123")
    config = load_config()
    assert config.api_key == "test-key-123"


def test_handles_missing_api_key(monkeypatch):
    monkeypatch.delenv("API_KEY", raising=False)
    with pytest.raises(ConfigError, match="API_KEY"):
        load_config()
```

Use `monkeypatch` for env vars. Use `mocker.patch` for replacing functions and methods.

---

## Anti-Patterns

1. **Mocking everything** — if a test mocks five things, it tests nothing. Mock only
   the boundary, then assert real behavior.
2. **Mocking implementation details** — don't mock internal helpers. If you refactor
   internals, tests shouldn't break.
3. **Brittle return chains** — `mock.return_value.foo.return_value.bar` is a sign
   you're testing the mock, not your code. Simplify the interface.
4. **Forgetting to assert calls** — a mock that's never checked is just dead code.
   Always verify the mock was actually used.
5. **Patching the wrong path** — patch where the name is *looked up*, not where it's
   *defined*. Patch `my_package.client.httpx.get`, not `httpx.get`.
