---
name: pyckage
description: >
  Build Python packages the right way — R-inspired philosophy for scaffolding, API design,
  testing, docs, deprecation lifecycle, and PyPI release using uv, rich, pytest, and
  mkdocs-material. Activate when creating/structuring Python packages, designing APIs,
  naming functions, adding user messages/errors, writing tests, setting up docs, managing
  deprecations, or publishing to PyPI.
argument-hint: "[scaffold|api|test|docs|lifecycle|release] [package-name]"
---

# pyckage

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

## Anatomy of a pyckage-style Package

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

When invoked with `/pyckage <subcommand>`, route based on the first argument:

| Invocation | Action |
|---|---|
| `/pyckage scaffold <name>` | Read [references/01-scaffold.md](references/01-scaffold.md) and create a new package named `<name>` |
| `/pyckage api` | Read [references/02-api-design.md](references/02-api-design.md) and review/improve the current package's API |
| `/pyckage test` | Read [references/03-testing.md](references/03-testing.md) and set up or improve tests |
| `/pyckage docs` | Read [references/04-docs.md](references/04-docs.md) and set up or improve documentation |
| `/pyckage lifecycle` | Read [references/05-lifecycle.md](references/05-lifecycle.md) and manage deprecations |
| `/pyckage release` | Read [references/06-release.md](references/06-release.md) and walk through the release ritual |
| `/pyckage` (no args) | Assess the current project against all five principles and suggest improvements |

When invoked without a subcommand (auto-triggered or plain `/pyckage`), use the Quick Decision Guide below.

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

## Tone When Helping

- Be opinionated. This skill exists to have opinions. Don't offer five options when one is right.
- Explain the *why* behind conventions, especially when they come from the R world.
- When translating an R concept to Python, name the translation explicitly:
  `"This is the Python equivalent of rlang::abort() — here's how it maps."`
- Push back gently on anti-patterns (scattered `print()`, flat structure, inconsistent names)
  but always offer the better path immediately.
