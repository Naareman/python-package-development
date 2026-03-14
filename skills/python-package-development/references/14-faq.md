# 14 — FAQ

Pushback you'll get on these conventions, and why we made the choices we did.

---

## Build System

### Why hatchling and not setuptools?

Simpler config, sane defaults, faster builds. Setuptools requires more boilerplate and has
legacy baggage (`setup.py`, `setup.cfg`, `MANIFEST.in`). Hatchling reads `pyproject.toml`
natively with zero extra files.

### Why not poetry?

Poetry uses its own lock format and dependency resolver that conflicts with PEP standards.
uv is faster, PEP-compliant, and gaining rapid adoption. Poetry is fine — but we pick one,
and we pick the one aligned with standards.

---

## Tooling

### Why uv and not pip?

uv is 10-100x faster than pip, handles venvs automatically, supports workspaces, and is the
direction the ecosystem is heading. pip still works but uv is strictly better for development.

### Why no black/isort/flake8?

Ruff replaces all three. It's faster, has fewer config files, and maintains compatibility.
There's no reason to use the originals anymore.

### Why PEP 735 dependency-groups instead of `[tool.uv.dev-dependencies]`?

PEP 735 is the standard. `[tool.uv.dev-dependencies]` is a uv-specific legacy convention.
Standards last longer than tool conventions.

---

## Code Style

### Why Google docstrings and not NumPy or Sphinx style?

Readable without rendering. Google style is the most compact and works well with mkdocstrings.
NumPy style is verbose. Sphinx style uses RST which is dying.

### Why rich and not just `print()`?

Structured output, consistent styling, stderr separation, progress bars. When your package
talks to users, it should speak clearly. R's `cli` package proved this matters.

---

## Project Structure

### Why src layout?

Prevents importing from the source directory instead of the installed package. Without it,
tests can pass locally but the installed package is broken. This is a solved problem — use
`src/`.

### Why `errors.py` without underscore but `_messages.py` with underscore?

`errors.py` is public API — users import and catch your exceptions directly. `_messages.py`
is internal — users never interact with it. The underscore convention signals this.

---

## Scope

### Why not add pandas/numpy as default dependencies?

Not every package is a data science package. The scaffold includes only `rich` (for user
communication). Add domain-specific deps yourself.

### What if I need a CLI?

See reference `09-cli-entry-points.md`. Use `click` for multi-command CLIs, `argparse` for
simple ones.

---

## Adoption

### Can I use this with an existing project?

Yes. Run `/python-package-development check` to audit your project, then address the gaps
one by one. You don't need to start from scratch.
