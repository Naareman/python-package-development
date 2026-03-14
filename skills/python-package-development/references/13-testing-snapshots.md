# 13 — Testing: Snapshots

R equivalent: `testthat::expect_snapshot()`. Snapshot tests capture complex output once,
then verify it doesn't change unexpectedly.

---

## When to Use Snapshots

Use them when the expected output is **complex, verbose, or tedious to write by hand**:

- Serialized data structures (JSON, YAML, dictionaries)
- Error messages and exception formatting
- CLI output and help text
- Rendered templates or reports
- Complex string representations (`__repr__`, `__str__`)

Do **not** use snapshots for:

- Simple equality checks (`assert x == 42` is clearer)
- Output that changes frequently (timestamps, random IDs)
- Performance-sensitive values (thresholds belong in explicit assertions)

---

## syrupy — Recommended Library

`syrupy` is the most actively maintained snapshot library for pytest.

```bash
uv add --dev syrupy
```

### Basic usage

```python
def test_report_output(snapshot):
    result = generate_report(year=2025, quarter=1)
    assert result == snapshot
```

On first run, syrupy creates a snapshot file in `__snapshots__/` next to your test file.
On subsequent runs, it compares the output against the stored snapshot.

### Snapshot of a specific attribute

```python
def test_error_message(snapshot):
    with pytest.raises(ValidationError) as exc_info:
        validate(bad_data)
    assert str(exc_info.value) == snapshot
```

---

## Updating Snapshots

When output changes intentionally, update the stored snapshots:

```bash
uv run pytest --snapshot-update
```

Always **review the diff** before committing updated snapshots. Treat snapshot updates
like code review — the diff should make sense.

---

## CLI Output Snapshots

Particularly useful for packages with a CLI interface:

```python
from click.testing import CliRunner

def test_help_output(snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])
    assert result.output == snapshot


def test_error_output(snapshot):
    runner = CliRunner()
    result = runner.invoke(cli, ["bad-command"])
    assert result.output == snapshot
    assert result.exit_code == 2
```

---

## Snapshot File Hygiene

- Commit `__snapshots__/` directories to version control
- Run `uv run pytest --snapshot-update` to remove orphaned snapshots
- Keep snapshots small — if a snapshot is 500 lines, consider testing individual
  components instead
- Add `__snapshots__/` to your `.gitattributes` as `linguist-generated` so they
  don't clutter pull request diffs

```gitattributes
**/__snapshots__/** linguist-generated=true
```
