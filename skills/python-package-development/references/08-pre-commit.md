# 08 — Pre-commit Hooks

R equivalent: integrating `lintr` + `styler` so they run automatically before every commit.
The goal is the same: catch formatting and lint issues before they reach the repo.

---

## What and Why

[pre-commit](https://pre-commit.com/) runs a set of checks automatically on `git commit`.
If any check fails, the commit is blocked until you fix the issue. This eliminates
"fix lint" commits and keeps the entire history clean.

---

## .pre-commit-config.yaml

Create this file at the repo root:

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: check-yaml
      - id: check-toml
      - id: end-of-file-fixer
      - id: trailing-whitespace

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.4.8
    hooks:
      - id: ruff            # linting (replaces flake8 + isort)
        args: [--fix]
      - id: ruff-format     # formatting (replaces black)

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.10.0
    hooks:
      - id: mypy
        additional_dependencies: []   # add stubs here, e.g. types-requests
        args: [--strict]
```

No need for `black`, `isort`, or `flake8` — ruff handles all three.

---

## Installation

```bash
# Add pre-commit as a dev dependency
uv add --group dev pre-commit

# Install the git hook (writes to .git/hooks/pre-commit)
uv run pre-commit install
```

After this, every `git commit` runs the hooks automatically on staged files only.

---

## Running Manually

```bash
# Run on all files (useful for first-time setup or CI)
uv run pre-commit run --all-files

# Run a specific hook
uv run pre-commit run ruff --all-files

# Update all hook versions to latest
uv run pre-commit autoupdate
```

---

## CI Integration

Add to your GitHub Actions workflow:

```yaml
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v4
      - run: uv sync --group dev
      - run: uv run pre-commit run --all-files
```

This catches anything that slipped past the local hook (force-pushed, hook not installed, etc.).

---

## Common Pitfall: Isolated Environments

Pre-commit runs each hook in its own isolated virtualenv. This means:

- The ruff version in pre-commit may differ from the one in your `uv.lock`
- mypy may see different stubs than your dev environment

**Fix:** Pin versions explicitly in `.pre-commit-config.yaml` (the `rev` field) and keep
them in sync with your `pyproject.toml` versions. Run `uv run pre-commit autoupdate`
periodically, then verify nothing breaks.

For mypy specifically, list any type stubs your code needs in `additional_dependencies`:

```yaml
      - id: mypy
        additional_dependencies: [types-requests, types-PyYAML]
```

---

## pyproject.toml — Keep Tool Config Centralized

Don't duplicate ruff or mypy config in the pre-commit config. The hooks read from
`pyproject.toml` automatically:

```toml
[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP"]

[tool.mypy]
python_version = "3.10"
strict = true
```

One source of truth. The pre-commit hooks and your `uv run ruff check` use the same rules.

---

## When to Skip Hooks

Rarely. But if you must:

```bash
git commit --no-verify -m "wip: broken but saving state"
```

This is for emergencies, not workflow. If you're skipping hooks regularly, fix the
underlying issue instead.
