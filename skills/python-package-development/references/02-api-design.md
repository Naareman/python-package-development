# 02 — API Design: Naming, Messages, and Errors

This is the heart of this skill's philosophy. R's tidyverse set a standard for what a
well-designed package API feels like. This reference encodes that standard for Python.

---

## Function Naming — The Grammar

### The verb_noun pattern
Functions should be named `verb_noun()`. Users learn the grammar and can predict names.

```python
# Good — follows the grammar
read_csv()
write_parquet()
validate_schema()
compute_summary()
filter_rows()

# Bad — unclear verb, or noun-first
csv_reader()
do_validation()
summary()        # too short, not guessable in context
```

### Families with shared prefixes
Related functions share a prefix. Users can tab-complete to discover the family.

```python
# A "read" family
read_csv()
read_parquet()
read_json()
read_excel()

# A "validate" family
validate_schema()
validate_types()
validate_range()
```

R equivalent: `readr`'s `read_*` family, `stringr`'s `str_*` family.

### Internal functions use a leading underscore
```python
def read_csv(path): ...          # public
def _parse_header(lines): ...    # internal, not exported
```

### Booleans use is_ / has_ / can_
```python
is_valid()
has_missing()
can_write()
```

---

## User Messages — The `rich` Hierarchy

Never use bare `print()`. All output goes through a centralized console in `_messages.py`.

### `_messages.py` — the message module

```python
from rich.console import Console

# One console for stdout (normal output)
console = Console()

# One console for stderr (errors, warnings)
err_console = Console(stderr=True)


def info(message: str) -> None:
    """Informational message — something is happening."""
    console.print(f"[bold blue]ℹ[/bold blue] {message}")


def success(message: str) -> None:
    """Something completed successfully."""
    console.print(f"[bold green]✓[/bold green] {message}")


def warn(message: str) -> None:
    """Non-fatal warning — something unexpected but recoverable."""
    err_console.print(f"[bold yellow]![/bold yellow] {message}")


def abort(message: str) -> None:
    """Fatal error message before raising an exception."""
    err_console.print(f"[bold red]✗[/bold red] {message}")
```

R equivalent: `cli::cli_inform()`, `cli::cli_warn()`, `cli::cli_abort()`.

### Message hierarchy — when to use what

| Situation | Function | R equivalent |
|---|---|---|
| Progress update | `info()` | `cli::cli_inform()` |
| Completed successfully | `success()` | `cli::cli_alert_success()` |
| Unexpected but recoverable | `warn()` | `cli::cli_warn()` |
| Fatal, about to raise | `abort()` then raise | `cli::cli_abort()` |

### With progress bars

```python
from rich.progress import track

def process_files(paths):
    for path in track(paths, description="Processing..."):
        _process_one(path)
```

---

## Structured Errors — `errors.py`

Errors are a public contract. Give users something they can catch specifically.
The file is named `errors.py` (no underscore) because error classes are part of the public API.

```python
# errors.py


class MyPackageError(Exception):
    """Base exception for my-package. Catch this to handle any package error."""
    pass


class ValidationError(MyPackageError):
    """Raised when input data fails validation."""

    def __init__(self, message: str, field: str | None = None):
        self.field = field
        super().__init__(message)


class FileFormatError(MyPackageError):
    """Raised when a file cannot be parsed."""

    def __init__(self, message: str, path: str | None = None):
        self.path = path
        super().__init__(message)
```

R equivalent: `rlang::abort()` with a condition class hierarchy.

### How to raise errors — always pair with `abort()`

```python
from my_package._messages import abort
from my_package.errors import ValidationError


def validate_schema(data, schema):
    if "id" not in data.columns:
        abort("Column 'id' is required but was not found.")
        raise ValidationError(
            "Missing required column: 'id'",
            field="id",
        )
```

This pattern: message first (visible, human-readable), then exception (catchable, structured).

**Trade-off:** `abort()` prints to stderr even if the caller catches the exception. This is intentional —
users running scripts should always see what went wrong. If you're building a library consumed by other
libraries (not end users), skip `abort()` and just raise the exception directly.

### What users can do with structured errors

```python
from my_package import validate_schema
from my_package.errors import ValidationError

try:
    validate_schema(df, schema)
except ValidationError as e:
    if e.field:
        print(f"Fix the '{e.field}' column")
```

---

## API Design Anti-Patterns to Avoid

| Anti-pattern | Why | Fix |
|---|---|---|
| `print(f"Error: {e}")` | Not catchable, not styled | Use `abort()` then raise |
| `raise Exception("bad")` | Too broad to catch | Use a specific error class |
| `do_thing_and_also_other_thing()` | Violates single responsibility | Split into two functions |
| Inconsistent naming (`get_data` vs `fetch_records`) | Breaks the grammar | Pick one verb family |
| Returning `None` on error silently | User has no idea what happened | Raise, don't return None |
