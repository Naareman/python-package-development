# 11 — Automated Release

Manual releases work (see [06-release.md](06-release.md)), but once your package is
mature, automate the ritual: commit, bump, tag, push, CI publishes.

---

## Conventional Commits

Standardize commit messages so tools can derive version bumps and changelogs:

```
feat: add streaming CSV reader          → minor bump (0.1.0 → 0.2.0)
fix: handle empty input in validate()   → patch bump (0.2.0 → 0.2.1)
feat!: redesign public API              → major bump (0.2.1 → 1.0.0)
chore: update dev dependencies          → no bump
docs: fix typo in docstring             → no bump
```

Prefix with scope if useful: `feat(io): add parquet support`.

---

## bump-my-version

Replaces the old `bump2version`. Reads config from `pyproject.toml`:

```toml
[tool.bumpversion]
current_version = "0.2.0"
commit = true
tag = true
tag_name = "v{new_version}"
message = "chore: release v{new_version}"

[[tool.bumpversion.files]]
filename = "pyproject.toml"
search = 'version = "{current_version}"'
replace = 'version = "{new_version}"'
# Only bump pyproject.toml — __version__ reads from metadata via importlib.metadata.version()
# No need to bump __init__.py when using the recommended single-source pattern
```

Usage:

```bash
uv run bump-my-version bump patch   # 0.2.0 → 0.2.1
uv run bump-my-version bump minor   # 0.2.0 → 0.3.0
uv run bump-my-version bump major   # 0.2.0 → 1.0.0
```

This edits files, commits, and creates a git tag in one step.

---

## Auto-Generating CHANGELOG

Use `git-cliff` or `towncrier` to generate CHANGELOG entries from commits.

With `git-cliff` (simpler, conventional-commit-based):

```bash
# Install
uv add --dev git-cliff

# Generate changelog from tags
uv run git-cliff --output CHANGELOG.md
```

Add a `cliff.toml` for customization, or configure in `pyproject.toml`.

---

## The Full Automated Flow

```
1. Write code, commit with conventional prefixes
2. Ready to release:
   $ uv run bump-my-version bump minor
     → edits version in pyproject.toml + __init__.py
     → commits: "chore: release v0.3.0"
     → tags: v0.3.0
3. Push:
   $ git push && git push --tags
4. CI takes over:
     → tag-triggered release.yml builds + publishes to PyPI
     → (see 06-release.md for the workflow YAML)
```

The release workflow in [06-release.md](06-release.md) already handles step 4 — it
triggers on `v*` tags and runs `uv build && uv publish`.

---

## CI Guardrail: Changelog Check

Add a PR check that warns if CHANGELOG is not updated:

```yaml
- name: Check CHANGELOG updated
  run: |
    git diff --name-only origin/main...HEAD | grep -q CHANGELOG.md \
      || echo "::warning::CHANGELOG.md was not updated"
```

---

## Summary

| Tool             | Role                              |
|------------------|-----------------------------------|
| Conventional commits | Standardize commit messages    |
| bump-my-version  | Bump version + commit + tag       |
| git-cliff        | Generate CHANGELOG from commits   |
| release.yml      | Tag-triggered PyPI publish (CI)   |
