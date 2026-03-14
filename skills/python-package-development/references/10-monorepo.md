# 10 — Monorepo and Namespace Packages

When you have multiple related packages in one repo (e.g., `mylib-core`, `mylib-io`,
`mylib-viz`), you need workspace tooling to manage them together.

---

## When to Use a Monorepo

- Several packages that share a release cadence or depend on each other
- A plugin ecosystem around a core library
- Internal packages that don't warrant separate repos

If you only have one package, don't do this. A single `pyproject.toml` is fine.

---

## uv Workspaces

Add a root `pyproject.toml` that declares workspace members:

```toml
# Root pyproject.toml — not a package itself
[project]
name = "my-workspace"
version = "0.0.0"

[tool.uv.workspace]
members = ["packages/*"]
```

Directory layout:

```
my-workspace/
├── pyproject.toml              ← workspace root (shared tooling config)
├── packages/
│   ├── mylib-core/
│   │   ├── pyproject.toml      ← per-package metadata + deps
│   │   └── src/mylib/core/
│   └── mylib-io/
│       ├── pyproject.toml
│       └── src/mylib/io/
```

Each member has its own `pyproject.toml` with its own `[project]` table, version, and
dependencies. Cross-references use `{ workspace = true }`:

```toml
# packages/mylib-io/pyproject.toml
[project]
name = "mylib-io"
version = "0.2.0"
dependencies = ["mylib-core"]

[tool.uv.sources]
mylib-core = { workspace = true }
```

---

## Namespace Packages (PEP 420, implemented in Python 3.3)

Namespace packages let multiple distributions share a top-level import path.
`mylib-core` provides `mylib.core`, `mylib-io` provides `mylib.io`, etc.

The key rule: **no `__init__.py` in the shared namespace directory**.

```
src/
└── mylib/              ← NO __init__.py here (implicit namespace package)
    └── core/
        └── __init__.py ← regular package starts here
```

Regular packages have `__init__.py` at every level. Namespace packages omit it at the
shared root so Python merges contributions from multiple installed packages.

---

## Shared Tooling Config

Put linting and type-checking config at the workspace root so all packages follow the
same rules:

```toml
# Root pyproject.toml
[tool.ruff]
src = ["packages/*/src"]
line-length = 88

[tool.mypy]
packages = ["mylib"]
strict = true
```

Run from root: `uv run ruff check .` and `uv run mypy .`

---

## Testing Across Packages

Each package has its own `tests/` directory. Run them individually or all at once:

```bash
# Single package
uv run --package mylib-core pytest packages/mylib-core/tests

# All packages from root
uv run pytest packages/*/tests
```

For integration tests that span packages, put them in a top-level `tests/` directory
at the workspace root.

---

## When Not to Use Namespace Packages

- If users will never `pip install` subsets independently, use a regular package
- If you need `__init__.py` logic (re-exports, lazy imports) at the top level
- If the complexity isn't justified — most projects are fine as a single package
