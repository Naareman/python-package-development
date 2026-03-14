# 05 — Lifecycle: Deprecation and Versioning

R equivalent: the `lifecycle` package. The principle: **breaking changes are promises
broken. Deprecations are promises kept.**

Never silently remove or change something. Always give users a path forward.

---

## Semantic Versioning — The Contract

Follow [semver](https://semver.org/) strictly:

| Change | Version bump | Example |
|---|---|---|
| Bug fix, no API change | Patch: `0.1.0 → 0.1.1` | Fix CSV parsing bug |
| New feature, backward compatible | Minor: `0.1.0 → 0.2.0` | Add `read_parquet()` |
| Breaking change | Major: `0.1.0 → 1.0.0` | Rename `read_data()` |

Before `1.0.0`, minor bumps can be breaking. Communicate this clearly in the README.

R equivalent: `usethis::use_version()` + the `lifecycle` package's stability badges.

---

## The Deprecation Ceremony

Deprecating something is a three-step process across versions:

### Step 1 — Warn (current version)
Keep the old function. Add a `DeprecationWarning`. Point to the new thing.

```python
import warnings
from my_package._messages import warn


def read_data(path):  # OLD name
    """Read data from a file.

    .. deprecated:: 0.3.0
        Use :func:`read_csv` instead. Will be removed in 0.5.0.
    """
    warn(
        "'read_data()' is deprecated and will be removed in v0.5.0. "
        "Use 'read_csv()' instead."
    )
    warnings.warn(
        "'read_data()' is deprecated, use 'read_csv()' instead.",
        DeprecationWarning,
        stacklevel=2,  # points to the caller, not this function
    )
    return read_csv(path)
```

`stacklevel=2` is critical — it makes the warning point to the user's code, not yours.

R equivalent: `lifecycle::deprecate_warn()`.

### Step 2 — Remind (next minor version)
Keep the function, escalate to a louder warning if needed. Update the "removed in" version.

### Step 3 — Remove (the version you promised)
Delete the function. Add to CHANGELOG under "Breaking Changes."

---

## Deprecation Helper

For consistent deprecation messages, add to `_messages.py`:

```python
import warnings


def deprecated(old_name: str, new_name: str, version: str) -> None:
    """Emit a standardized deprecation warning.

    Args:
        old_name: The function or argument being deprecated.
        new_name: What to use instead.
        version: The version when it will be removed.
    """
    warn(
        f"'{old_name}' is deprecated and will be removed in v{version}. "
        f"Use '{new_name}' instead."
    )
    warnings.warn(
        f"'{old_name}' is deprecated, use '{new_name}' instead.",
        DeprecationWarning,
        stacklevel=3,  # 3 because: user_code -> wrapper_func -> deprecated() -> warnings.warn
    )
```

Usage:
```python
def read_data(path):
    deprecated("read_data", "read_csv", version="0.5.0")
    return read_csv(path)
```

---

## Deprecating Arguments

When an argument is renamed or removed:

```python
def read_csv(path, *, charset=None, encoding="utf-8"):
    """..."""
    if charset is not None:
        deprecated("charset", "encoding", version="0.5.0")
        encoding = charset
    # use encoding going forward
```

---

## CHANGELOG — The User-Facing History

The CHANGELOG is for users, not developers. Every release gets an entry.

```markdown
# Changelog

## Unreleased

## 0.3.0 — 2025-06-01

### Added
- `read_parquet()` for reading Parquet files (#42)

### Deprecated
- `read_data()` is deprecated; use `read_csv()` instead. Will be removed in 0.5.0.

### Fixed
- `validate_schema()` now handles empty DataFrames correctly (#39)

## 0.2.0 — 2025-03-15

### Breaking Changes
- `parse_file()` renamed to `read_csv()`. Update your imports.

### Added
- `write_csv()` for writing DataFrames to disk
```

R equivalent: `NEWS.md` in tidyverse packages.

### Rules for CHANGELOG entries

- **Breaking Changes** go first and are always explicit
- **Added** — new public functions or arguments
- **Deprecated** — always include what to use instead and when it's removed
- **Fixed** — bug fixes with issue numbers if possible
- **Removed** — things that were deprecated and are now gone

---

## Version in One Place

Set the version in `pyproject.toml` only. Read it in `__init__.py` dynamically:

```python
# src/my_package/__init__.py
from importlib.metadata import version

__version__ = version("my-package")
```

Never hardcode the version in two places.
