# 07 — Common Mistakes in Python Packaging

These are real-world mistakes that trip up both beginners and experienced developers.
When reviewing or writing package code, check for these actively.

---

## Table of Contents

- [Project Structure](#project-structure)
- [pyproject.toml Configuration](#pyprojecttoml-configuration)
- [Imports](#imports)
- [Version Management](#version-management)
- [Dependencies](#dependencies)
- [Files Missing from Builds](#files-missing-from-builds)
- [Publishing](#publishing)
- [Testing](#testing)

---

## Project Structure

### Using flat layout instead of src layout
```
# BAD — source is importable from project root
my-package/
├── my_package/    ← Python imports this instead of installed version
├── tests/
└── pyproject.toml

# GOOD — src layout prevents accidental imports
my-package/
├── src/
│   └── my_package/
├── tests/
└── pyproject.toml
```
**Why:** The current working directory is first on `sys.path`. Without `src/`, tests pass
locally but the installed package may be broken (missing files, wrong imports).

### Including tests/ in the wheel
**Mistake:** Build includes a top-level `tests/` in the wheel.
**Why:** Writes to `site-packages/tests/`, colliding with other packages.
**Fix:** With src layout + `packages = ["src/my_package"]`, tests are excluded automatically.
For flat layouts, explicitly exclude: `[tool.hatch.build.targets.wheel] exclude = ["tests"]`.

### Putting `__init__.py` in tests/
**Why:** Confuses package discovery. Tests should never be importable.
**Fix:** Remove it. Use `conftest.py` for shared fixtures.

---

## pyproject.toml Configuration

### Missing `[build-system]` table
**Why:** Build tools fall back to legacy setuptools behavior, which is unpredictable.
**Fix:** Always include:
```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### Deprecated license table format
**Mistake:** `license = {text = "MIT"}` or `license = {file = "LICENSE"}`.
**Why:** PEP 639 deprecated the table format.
**Fix:** Use `license = "MIT"` (SPDX string) + `license-files = ["LICENSE"]`.

### Not reinstalling after changing pyproject.toml
**Why:** `pyproject.toml` is read at install time. Changes are ignored until reinstall.
**Fix:** Run `uv sync` or `uv pip install -e .` after changes.

---

## Imports

### Running modules directly instead of `python -m`
**Mistake:** `python src/mypackage/cli.py`
**Why:** Sets `__package__` to `None`, breaking all relative imports.
**Fix:** Use `python -m mypackage.cli`, or define entry points:
```toml
[project.scripts]
mycli = "mypackage.cli:main"
```

### "Import the world" in `__init__.py`
```python
# BAD
from .models import *
from .utils import *
from .core import *

# GOOD
from my_package.core import read_data, write_data
from my_package.errors import MyPackageError

__all__ = ["read_data", "write_data", "MyPackageError"]
```
**Why:** Slows import time, wastes memory, pollutes namespace.

### Missing `__all__` for re-exports
**Why:** Type checkers (mypy, pyright) treat imports without `__all__` as private.
Users get "module has no attribute" type errors.

### `TYPE_CHECKING` guard without string annotations
```python
# BAD — crashes at runtime
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .models import User

def get_user() -> User: ...  # NameError!

# GOOD — use string annotation or future annotations
from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .models import User

def get_user() -> User: ...  # works
```

---

## Version Management

### Version in multiple places
**Mistake:** Hardcoding in both `pyproject.toml` and `__init__.py`.
**Fix:** Single source:
```python
# src/my_package/__init__.py
from importlib.metadata import version
__version__ = version("my-package")
```

### Dynamic version that isn't a string literal
**Mistake:** `__version__ = f"{major}.{minor}.{patch}"` or `__version__ = get_version()`.
**Why:** Build backends parse source statically — they won't execute your code.
**Fix:** Always a plain string: `__version__ = "1.2.3"` (if not using importlib.metadata).

### importlib.metadata with no fallback
**Mistake:** Fails when code is copied without installing (Lambda, Docker, vendoring).
**Fix:**
```python
try:
    from importlib.metadata import version, PackageNotFoundError
    __version__ = version("my-package")
except PackageNotFoundError:
    __version__ = "0.0.0"
```

---

## Dependencies

### No version bounds
**Mistake:** `dependencies = ["requests", "pydantic"]`
**Fix:** Lower bounds: `dependencies = ["requests>=2.28", "pydantic>=2.0"]`

### Overly strict upper bounds
**Mistake:** `dependencies = ["requests>=2.28,<3"]`
**Why:** When a compatible release comes out, your package blocks users from upgrading.
This is the single biggest cause of dependency resolution conflicts in Python.
**Fix:** Lower bounds only for libraries. Reserve upper bounds for *known* incompatibilities.

### Upper bound on `requires-python`
**Mistake:** `requires-python = ">=3.10,<3.13"`
**Why:** pip/uv will refuse to install on Python 3.13 even though it almost certainly works.
**Fix:** `requires-python = ">=3.10"`

### Pinned exact versions in library deps
**Mistake:** `dependencies = ["requests==2.31.0"]`
**Why:** Makes it impossible to install alongside other packages needing a different version.
**Fix:** Pins are for applications (lock files), not libraries.

### Dev deps in `[project] dependencies`
**Mistake:** pytest, ruff, mypy in `dependencies`.
**Why:** Users installing your library get all your dev tools as transitive deps.
**Fix:** Use `[dependency-groups]` (PEP 735):
```toml
[dependency-groups]
dev = ["pytest>=8.0", "ruff>=0.4", "mypy>=1.0"]
```

---

## Files Missing from Builds

### `py.typed` not shipping in wheel
**Why:** Type checkers treat your package as untyped and ignore all annotations.
**Fix:** Verify: `unzip -l dist/*.whl | grep py.typed`

### Non-Python data files missing
**Mistake:** JSON schemas, templates, SQL files at project root instead of inside package dir.
**Fix:** Put data files inside `src/my_package/`. Hatchling includes them by default.

### Confusing MANIFEST.in with wheel contents
**Why:** `MANIFEST.in` only controls sdist (source distribution). Zero effect on wheels.
**Fix:** Use build backend config for wheel contents.

---

## Publishing

### Not building both sdist and wheel
**Why:** Without wheel: slow source builds. Without sdist: users can't audit source.
**Fix:** `uv build` produces both by default.

### Classifiers not matching `requires-python`
**Mistake:** `requires-python = ">=3.10"` but classifiers only list 3.10, 3.11.
**Why:** PyPI uses classifiers for search filtering. Not auto-generated.
**Fix:** Keep classifiers in sync with every Python version you test against.

### Not using Trusted Publishing
**Mistake:** Long-lived API tokens in CI secrets.
**Why:** Tokens can leak. Compromised CI = malicious package versions.
**Fix:** Use PyPI Trusted Publishing (OIDC) with GitHub Actions.

---

## Testing

### Testing source checkout instead of installed package
**Why:** Missing files, wrong `__init__.py`, broken entry points — none caught.
**Fix:** src layout + editable install (`uv pip install -e .`) + pytest.

### Importing from conftest.py explicitly
**Mistake:** `from conftest import some_fixture`
**Why:** conftest.py is auto-loaded by pytest. Explicit imports cause double-loading.
**Fix:** Just use fixture names — pytest injects them automatically.
