# 06 — Release: PyPI and GitHub Actions

R equivalent: `devtools::release()` + CRAN submission. PyPI is easier than CRAN but
still deserves ceremony. Don't publish carelessly.

---

## Pre-Release Checklist

Run this before every release:

```bash
# 1. All tests pass
uv run pytest

# 2. No linting errors
uv run ruff check src/

# 3. Types check out
uv run mypy src/

# 4. Docs build cleanly
uv run mkdocs build --strict

# 5. CHANGELOG.md is updated — move "Unreleased" to the new version
# 6. Version is bumped in pyproject.toml
# 7. Everything is committed and pushed
```

R equivalent: `devtools::check()` before `devtools::release()`.

---

## Bumping the Version

Edit `pyproject.toml` manually, or use:

```bash
# With uv (manual)
# Edit version = "0.2.0" in pyproject.toml

# Commit the bump
git add pyproject.toml CHANGELOG.md
git commit -m "chore: release v0.2.0"
git tag v0.2.0
git push && git push --tags
```

---

## Publishing to PyPI

```bash
# Build the package
uv build

# Check what was built
ls dist/
# my_package-0.2.0-py3-none-any.whl
# my_package-0.2.0.tar.gz

# Upload to PyPI (first time: uv publish --token YOUR_TOKEN)
uv publish
```

Set up a PyPI API token and store it as a GitHub secret (`PYPI_TOKEN`) for CI.

---

## GitHub Actions — CI/CD

### `.github/workflows/ci.yml` — run on every push and PR

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.10", "3.11", "3.12"]

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Set up Python ${{ matrix.python-version }}
        run: uv python install ${{ matrix.python-version }}

      - name: Install dependencies
        run: uv sync --all-extras --dev

      - name: Lint
        run: uv run ruff check src/

      - name: Type check
        run: uv run mypy src/

      - name: Test
        run: uv run pytest
```

### `.github/workflows/release.yml` — publish on tagged release

```yaml
name: Release

on:
  push:
    tags:
      - "v*"

jobs:
  publish:
    runs-on: ubuntu-latest
    environment: pypi
    permissions:
      id-token: write  # for trusted publishing

    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Build
        run: uv build

      - name: Publish to PyPI
        run: uv publish
        # If not using trusted publishing, add:
        # env:
        #   UV_PUBLISH_TOKEN: ${{ secrets.PYPI_TOKEN }}
```

Using PyPI's trusted publishing (OIDC) is preferred over API tokens — no secrets needed.
You must configure your PyPI project as a trusted publisher first (link below), otherwise
`uv publish` will fail with an auth error. Alternative: set `PYPI_TOKEN` as a GitHub secret.
Set it up at: https://pypi.org/manage/account/publishing/

### `.github/workflows/docs.yml` — deploy docs on push to main

```yaml
name: Docs

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        uses: astral-sh/setup-uv@v3

      - name: Install dependencies
        run: uv sync --dev

      - name: Deploy docs
        run: uv run mkdocs gh-deploy --force
```

---

## The Release Ritual

Think of this like `devtools::release()` asking you the checklist questions:

1. **Is the version bumped?** Check `pyproject.toml`
2. **Is CHANGELOG updated?** "Unreleased" → version + date
3. **Do all tests pass?** `uv run pytest`
4. **Does the README example still work?** Run it manually
5. **Is there a git tag?** `git tag v0.2.0`
6. **Is the tag pushed?** `git push --tags` (triggers the release workflow)

After release:
- Check PyPI that the new version is live: `pip install my-package==0.2.0`
- Check that docs deployed correctly
- Open a new "Unreleased" section in CHANGELOG
