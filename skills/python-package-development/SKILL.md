---
name: python-package-development
description: >
  Build Python packages the right way — R-inspired philosophy for scaffolding, API design,
  testing, docs, deprecation lifecycle, and PyPI release using uv, rich, pytest, and
  mkdocs-material. Activate when creating/structuring Python packages, designing APIs,
  naming functions, adding user messages/errors, writing tests, setting up docs, managing
  deprecations, or publishing to PyPI.
argument-hint: "[scaffold|api|test|docs|lifecycle|release|check|pre-commit|cli] [package-name]"
---

# python-package-development

A skill for building Python packages with the philosophy of the R package ecosystem:
clear user communication, principled API design, living documentation, and ceremonial lifecycle management.

The guiding question for every decision: *"What would make this package feel like a thoughtful, professional tool — not just a collection of functions?"*

---

## How This Skill Is Organized

This SKILL.md gives you the philosophy and the map. For implementation details, read the
relevant reference file from `references/`:

| What you're doing | Read |
|---|---|
| Starting a new package or setting up structure | [references/01-scaffold.md](references/01-scaffold.md) |
| Designing function names, errors, user messages | [references/02-api-design.md](references/02-api-design.md) |
| Writing or organizing tests | [references/03-testing.md](references/03-testing.md) |
| Setting up or writing documentation | [references/04-docs.md](references/04-docs.md) |
| Adding deprecations or managing versions | [references/05-lifecycle.md](references/05-lifecycle.md) |
| Releasing to PyPI or setting up CI/CD | [references/06-release.md](references/06-release.md) |
| Auditing for common anti-patterns | [references/07-common-mistakes.md](references/07-common-mistakes.md) |
| Setting up pre-commit hooks | [references/08-pre-commit.md](references/08-pre-commit.md) |
| Adding a CLI to your package | [references/09-cli-entry-points.md](references/09-cli-entry-points.md) |
| Managing a monorepo / namespace packages | [references/10-monorepo.md](references/10-monorepo.md) |
| Automating releases (bump, changelog, CI) | [references/11-automated-release.md](references/11-automated-release.md) |
| Mocking in tests (APIs, filesystem, time) | [references/12-testing-mocking.md](references/12-testing-mocking.md) |
| Snapshot testing | [references/13-testing-snapshots.md](references/13-testing-snapshots.md) |
| FAQ (why these opinions?) | [references/14-faq.md](references/14-faq.md) |

Read only what's relevant to the current task. Don't load everything at once.

---

## The Five Principles

Before touching any reference file, internalize these. They inform every decision.

### 1. User communication is a first-class concern
Every message a user sees — errors, warnings, progress, success — should be intentional.
Use `rich` for structure and color. Use a consistent message hierarchy. Never let a raw
traceback be the user's only feedback. The R `cli` package set this standard; `rich` is how
we meet it in Python.

### 2. Function names form a grammar
Names should be guessable. Use `verb_noun()` patterns. Group related functions with shared
prefixes. A user should be able to predict `read_parquet()` after seeing `read_csv()`.
Consistency is more important than cleverness.

### 3. Lifecycle deserves ceremony
Deprecations are promises to users. When something changes, warn early, warn clearly, and
give users a path forward. Never silently break things. Never deprecate without a timeline.

### 4. Documentation lives next to code
Docstrings are not optional and not a final step. They are written at the same time as the
function. Use Google style consistently. `mkdocstrings` turns them into a website automatically.

### 5. There is a whole game
A user should be able to see a complete, working package early — not after mastering every
detail. Scaffold first, refine later.

---

## Anatomy of a Well-Structured Package

```
my-package/
├── pyproject.toml          ← single source of truth (uv-managed)
├── README.md               ← the story and quickstart
├── CHANGELOG.md            ← user-facing version history
├── mkdocs.yml              ← docs config (project root, not inside docs/)
├── src/
│   └── my_package/
│       ├── __init__.py     ← clean public API surface
│       ├── py.typed         ← PEP 561 marker for type checkers
│       ├── errors.py       ← structured exception hierarchy (public contract)
│       ├── _messages.py    ← rich console, message helpers
│       └── core.py         ← actual logic
├── tests/
│   ├── conftest.py         ← shared fixtures
│   └── test_core.py
└── docs/
    ├── index.md
    └── api.md
```

Key decisions encoded here:
- **src layout** always — prevents accidental imports from the project root
- **`errors.py`** is always its own file — errors are a public contract (no underscore: users import these directly)
- **`_messages.py`** centralizes all user-facing output — never scattered `print()` calls
- **`__init__.py`** is curated, not auto-imported — users see only what's intentional

---

## Argument Routing

When invoked with `/python-package-development <subcommand>`, route based on the first argument:

| Invocation | Action |
|---|---|
| `/python-package-development scaffold <name>` | Read [references/01-scaffold.md](references/01-scaffold.md) and create a new package named `<name>` |
| `/python-package-development api` | Read [references/02-api-design.md](references/02-api-design.md) and review/improve the current package's API |
| `/python-package-development test` | Read [references/03-testing.md](references/03-testing.md) and set up or improve tests |
| `/python-package-development docs` | Read [references/04-docs.md](references/04-docs.md) and set up or improve documentation |
| `/python-package-development lifecycle` | Read [references/05-lifecycle.md](references/05-lifecycle.md) and manage deprecations |
| `/python-package-development release` | Read [references/06-release.md](references/06-release.md) and walk through the release ritual |
| `/python-package-development check` | Run `python ${CLAUDE_SKILL_DIR}/../../scripts/check-structure.py .` then read [references/07-common-mistakes.md](references/07-common-mistakes.md) to fix any failures |
| `/python-package-development pre-commit` | Read [references/08-pre-commit.md](references/08-pre-commit.md) and set up pre-commit hooks |
| `/python-package-development cli` | Read [references/09-cli-entry-points.md](references/09-cli-entry-points.md) and add a CLI to the package |
| `/python-package-development` (no args) | Assess the current project against all five principles (see checklist below) |

When invoked without a subcommand (auto-triggered or plain `/python-package-development`):

**Step 1 — Automated audit.** Run the convention checker if available:
```
python ${CLAUDE_SKILL_DIR}/../../scripts/check-structure.py .
```

**Step 2 — Manual review** of things the script can't check:
1. **Naming** — Do public functions follow `verb_noun()`? Are families consistent?
2. **Documentation** — Do all public functions have Google-style docstrings with Args/Returns/Raises?
3. **Messages** — Is `_messages.py` actually used? Any bare `print()` calls?
4. **Lifecycle** — Is `__version__` from `importlib.metadata`? Any undocumented breaking changes?

**Step 3 — Suggest improvements** using the Quick Decision Guide below.

---

## Quick Decision Guide

**User asks to scaffold / create a new package:**
→ Read [references/01-scaffold.md](references/01-scaffold.md). Walk through the whole game first.

**User asks about function names, API shape, or error messages:**
→ Read [references/02-api-design.md](references/02-api-design.md). Apply naming conventions and message hierarchy.

**User asks about tests or is writing test code:**
→ Read [references/03-testing.md](references/03-testing.md). Enforce pytest conventions and fixture patterns.

**User asks about docs, docstrings, or mkdocs:**
→ Read [references/04-docs.md](references/04-docs.md). Enforce Google docstrings and mkdocs-material setup.

**User mentions deprecating something, versioning, or breaking changes:**
→ Read [references/05-lifecycle.md](references/05-lifecycle.md). Apply the deprecation ceremony.

**User wants to publish, release, or set up CI:**
→ Read [references/06-release.md](references/06-release.md). Walk through PyPI + GitHub Actions setup.

**Multiple concerns at once:**
→ Read the most relevant reference first. Reference others by name when needed.

---

## Common Mistakes — Catch These Early

When reviewing or generating Python package code, watch for these. If you see any, fix them
immediately and explain why.

| Mistake | Why it's bad | Fix |
|---|---|---|
| Flat layout (no `src/`) | Imports source dir instead of installed package — tests pass locally, fail for users | Always use `src/` layout |
| `from .module import *` in `__init__.py` | Slow imports, polluted namespace, no control over public API | Explicit imports + `__all__` |
| `--cov=src` in pytest | Measures directory path, not importable module — confusing reports | `--cov=my_package` (the importable name) |
| `dependencies = ["requests"]` (no version) | Breaking release silently breaks your package | Lower bound: `"requests>=2.28"` |
| `dependencies = ["requests>=2.28,<3"]` | Blocks users from upgrading — #1 cause of dependency conflicts | Lower bound only for libraries |
| `requires-python = ">=3.10,<3.13"` | Blocks install on new Python versions that almost certainly work | Lower bound only: `">=3.10"` |
| `__version__ = "0.1.0"` hardcoded in two places | Version drift between pyproject.toml and code | Use `importlib.metadata.version()` |
| Missing `py.typed` marker | Type checkers ignore all your annotations for downstream users | `touch src/my_package/py.typed` |
| `print()` for user messages | Not styled, not catchable, not centralized | Use `_messages.py` with `rich` |
| `raise Exception("bad")` | Too broad — users can't catch specific errors | Custom exception hierarchy in `errors.py` |
| Dev deps in `[project] dependencies` | Users get pytest, ruff installed as transitive deps | Use `[dependency-groups]` (PEP 735) |
| `tests/__init__.py` exists | Confuses package discovery, may ship tests in wheel | Remove it — use `conftest.py` instead |
| `MANIFEST.in` for wheel contents | MANIFEST.in only affects sdist, not wheels | Use build backend config for wheel contents |
| Pinned deps in library (`"requests==2.31.0"`) | Impossible to install alongside anything else needing requests | Pins are for apps (lock files), not libraries |
| `mkdocs.yml` inside `docs/` | `mkdocs serve` looks in project root by default | Keep `mkdocs.yml` at project root |

For the full list with detailed explanations, see [references/07-common-mistakes.md](references/07-common-mistakes.md).

---

## Tone When Helping

- Be opinionated. This skill exists to have opinions. Don't offer five options when one is right.
- Explain the *why* behind conventions, especially when they come from the R world.
- When translating an R concept to Python, name the translation explicitly:
  `"This is the Python equivalent of rlang::abort() — here's how it maps."`
- Push back gently on anti-patterns (scattered `print()`, flat structure, inconsistent names)
  but always offer the better path immediately.
