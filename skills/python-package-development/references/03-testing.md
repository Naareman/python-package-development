# 03 — Testing

R equivalent: `testthat`. The goal is the same: tests should be easy to write, easy to
read, and impossible to accidentally skip.

---

## Structure

```
tests/
├── conftest.py          ← shared fixtures (the testthat equivalent of helper files)
├── test_core.py         ← tests for core.py
├── test_errors.py       ← tests for error behavior
└── data/                ← small test data files, if needed
    └── sample.csv
```

One test file per source module. Name them `test_<module>.py`.

---

## conftest.py — Shared Fixtures

```python
# tests/conftest.py
import pytest


@pytest.fixture
def sample_records():
    """A minimal list of dicts for testing."""
    return [
        {"id": 1, "value": 10.0},
        {"id": 2, "value": 20.0},
        {"id": 3, "value": 30.0},
    ]


@pytest.fixture
def empty_records():
    """An empty list — useful for edge case testing."""
    return []


@pytest.fixture
def tmp_csv(tmp_path, sample_records):
    """A temporary CSV file on disk."""
    path = tmp_path / "sample.csv"
    header = ",".join(sample_records[0].keys())
    rows = [",".join(str(v) for v in row.values()) for row in sample_records]
    path.write_text(header + "\n" + "\n".join(rows) + "\n")
    return path
```

R equivalent: `testthat`'s `helper-*.R` files and `local_*` fixtures.

---

## Writing Tests

### Basic structure — Arrange, Act, Assert

```python
def test_read_csv_returns_dataframe(tmp_csv):
    # Arrange — handled by fixture

    # Act
    result = read_csv(tmp_csv)

    # Assert
    assert isinstance(result, pd.DataFrame)
    assert len(result) == 3
    assert "id" in result.columns
```

### Test names — be descriptive

```python
# Good — tells you exactly what's being tested and what should happen
def test_validate_schema_raises_on_missing_id_column():
def test_read_csv_handles_empty_file():
def test_filter_rows_returns_empty_df_when_no_match():

# Bad — too vague
def test_validate():
def test_read():
def test_filter_2():
```

### Testing errors — always test the contract

```python
import pytest
from my_package.errors import ValidationError


def test_validate_schema_raises_validation_error_for_missing_column(sample_df):
    df = sample_df.drop(columns=["id"])

    with pytest.raises(ValidationError) as exc_info:
        validate_schema(df, schema={"required": ["id"]})

    assert exc_info.value.field == "id"
    assert "id" in str(exc_info.value)
```

R equivalent: `testthat::expect_error()` with a class argument.

### Testing warnings

```python
def test_deprecated_function_warns(sample_df):
    with pytest.warns(DeprecationWarning, match="use `read_csv` instead"):
        old_read_data(sample_df)
```

---

## Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run a single file
uv run pytest tests/test_core.py

# Run a single test
uv run pytest tests/test_core.py::test_read_csv_returns_dataframe

# Verbose output
uv run pytest -v
```

---

## Coverage

Coverage is configured in `pyproject.toml` (see scaffold reference). Aim for >90% on
core logic. Don't chase 100% — test behavior, not lines.

```toml
[tool.pytest.ini_options]
addopts = "--cov=my_package --cov-report=term-missing"  # use your importable package name
```

---

## What to Always Test

These are non-negotiable for a well-structured package:

1. **Happy path** — the normal case works
2. **Empty inputs** — empty DataFrame, empty list, empty string
3. **Error cases** — the right exception is raised with the right message/field
4. **Deprecation warnings** — deprecated functions actually warn
5. **Public API surface** — everything in `__init__.py` has at least one test

## What Not to Test

- Internal `_functions` that are implementation details (test via the public API)
- Third-party library behavior (don't test that `pandas` works)
- Type annotations (mypy handles this)
