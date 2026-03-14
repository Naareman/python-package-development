# 01 — Scaffold

The R equivalent: `usethis::create_package()` + `devtools`. The goal is to go from nothing
to a working, installable package in one session — the "whole game."

---

## The Whole Game (run this first)

```bash
# 1. Create the project
uv init my-package --lib
cd my-package

# 2. Set up src layout (uv --lib does this, but verify)
# Structure should be:
# src/my_package/__init__.py

# 3. Add core dependencies
uv add rich          # user messages
uv add --group dev pytest pytest-cov ruff mypy mkdocs-material mkdocstrings[python]

# 4. Initialize git
git init
git add .
git commit -m "chore: initial package scaffold"
```

That's the whole game. You now have an installable package. Everything else is refinement.

---

## pyproject.toml — The Single Source of Truth

This replaces R's `DESCRIPTION` file. It should contain everything:

```toml
[project]
name = "my-package"
version = "0.1.0"
description = "One clear sentence describing what this does."
readme = "README.md"
license = "MIT"
license-files = ["LICENSE"]
authors = [{ name = "Your Name", email = "you@example.com" }]
requires-python = ">=3.10"
classifiers = [
    "Programming Language :: Python :: 3.10",
    "Programming Language :: Python :: 3.11",
    "Programming Language :: Python :: 3.12",
    "Programming Language :: Python :: 3.13",
]
dependencies = [
    "rich>=13.0",
]

[project.urls]
Homepage = "https://github.com/you/my-package"
Documentation = "https://you.github.io/my-package"
Repository = "https://github.com/you/my-package"

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
    "ruff>=0.4",
    "mypy>=1.0",
    "mkdocs-material>=9.0",
    "mkdocstrings[python]>=0.25",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/my_package"]

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "--cov=my_package --cov-report=term-missing"  # use your importable package name, not "src"

[tool.mypy]
python_version = "3.10"
strict = true
```

---

## The src Layout — Always

Never use a flat layout. The src layout prevents a class of subtle bugs where Python
imports your source directory instead of the installed package.

```
my-package/           ← repo root (never import from here)
├── src/
│   └── my_package/   ← importable package lives here
│       ├── __init__.py
│       ├── py.typed
│       ├── errors.py
│       ├── _messages.py
│       └── core.py
├── tests/
├── docs/
└── pyproject.toml
```

R equivalent: the strict separation between the package directory and the project directory.

---

## `__init__.py` — Curate the Public API

Don't auto-import everything. Be explicit. This is the user's entry point.

```python
"""my-package: one clear sentence about what this does."""

from importlib.metadata import version

from my_package.core import read_data, transform_data, write_data
from my_package.errors import MyPackageError, ValidationError

__all__ = [
    "read_data",
    "transform_data",
    "write_data",
    "MyPackageError",
    "ValidationError",
]

__version__ = version("my-package")  # add PackageNotFoundError fallback if needed (see 07-common-mistakes.md)
```

R equivalent: the `NAMESPACE` file — explicit exports only.

---

## Files to Create at Scaffold Time

Beyond the Python files, always create:

**`.gitignore`** — include `.venv/`, `dist/`, `__pycache__/`, `.mypy_cache/`, `htmlcov/`

**`.python-version`** — pin your development Python version (e.g., `3.12`). uv uses this automatically.

**`py.typed`** — empty marker file in `src/my_package/py.typed` (PEP 561). This tells type checkers
that your package ships inline types. Create it with `touch src/my_package/py.typed`.

**`CHANGELOG.md`** — start it now, even if empty:
```markdown
# Changelog

## Unreleased
- Initial release
```

**`README.md`** — must include: what it does (one sentence), installation, quickstart example.

---

## After Scaffolding — Verify It Works

```bash
uv run python -c "import my_package; print(my_package.__version__)"
uv run pytest
uv run ruff check src/
uv run mypy src/
```

If all four pass, the scaffold is done. Commit before moving on.
