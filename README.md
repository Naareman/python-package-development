# python-package-development

> *"Just as Hadley Wickham brought the Grammar of Graphics to R as ggplot2, this skill brings the philosophy of R package development to Python."*

## What is this?

**python-package-development** is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that teaches Claude how to build Python packages the right way — using the hard-won wisdom of the R package ecosystem.

Python has incredible packages. But it has never had a unified philosophy for *building* them. The R world has one: Hadley Wickham's [*R Packages*](https://r-pkgs.org/) book (with Jenny Bryan), backed by tools like `devtools`, `usethis`, `roxygen2`, `cli`, and `lifecycle`.

This skill translates that philosophy into Python using modern tools: `uv`, `rich`, `pytest`, and `mkdocs-material`.

> Looking for the CLI tool? See [packright](https://github.com/Naareman/packright) — the companion Python package that automates these conventions from the command line.

## Installation

### For all your projects (personal scope)

```bash
git clone https://github.com/Naareman/python-package-development.git
cp -r python-package-development ~/.claude/skills/python-package-development
```

### For a single project (project scope)

```bash
mkdir -p .claude/skills
cp -r /path/to/python-package-development .claude/skills/python-package-development
```

### Verify it's installed

In Claude Code, run `/python-package-development` — you should see it in the skill list.

## Usage

The skill activates automatically when you're working on Python package tasks. You can also invoke it explicitly:

```
/python-package-development scaffold my-new-package
/python-package-development api
/python-package-development test
/python-package-development docs
/python-package-development lifecycle
/python-package-development release
/python-package-development check
/python-package-development pre-commit
/python-package-development cli
/python-package-development
```

Or just describe what you need — the skill activates when it recognizes a Python packaging task:

- *"I want to make a Python library"*
- *"Help me structure my code as a package"*
- *"How should I name these functions?"*
- *"How do I publish to PyPI?"*

## The Philosophy (what R taught us)

### 1. User communication is a first-class concern
R's `cli` package made beautiful, structured messages easy. This skill brings that to Python through `rich` and structured exception hierarchies.

### 2. Function names form a grammar
Tidyverse packages use `verb_noun()` consistently. Users can *guess* function names because the grammar is predictable.

### 3. Lifecycle deserves ceremony
R's `lifecycle` package gave deprecations a formal process. Users are never surprised.

### 4. Documentation lives next to code
`roxygen2` made it impossible to forget documentation. This skill enforces Google-style docstrings + `mkdocstrings`.

### 5. There is a whole game
Before diving into details, you should see the whole thing working end-to-end.

## What This Skill Covers

| Stage | R equivalent | Python |
|---|---|---|
| Scaffold | `usethis::create_package()` | `uv init` + src layout |
| Dependency management | `DESCRIPTION` + `devtools` | `pyproject.toml` + `uv` |
| User messages | `cli` package | `rich` Console |
| Structured errors | `rlang::abort()` | Custom exception hierarchy |
| API naming | tidyverse conventions | `verb_noun`, families, prefixes |
| Testing | `testthat` | `pytest` + fixtures |
| Documentation | `roxygen2` + `pkgdown` | Google docstrings + `mkdocs-material` |
| Lifecycle | `lifecycle` package | `warnings` + deprecation conventions |
| Release | `devtools::release()` | GitHub Actions + PyPI |

## Skill Structure

```
python-package-development/
├── SKILL.md                          # Main skill definition (philosophy + routing)
├── README.md                         # This file
├── examples/
│   └── my-package/                   # Complete reference implementation (22/22 checks)
├── references/
│   ├── 01-scaffold.md                # Package scaffolding (the "whole game")
│   ├── 02-api-design.md              # Naming, messages, errors
│   ├── 03-testing.md                 # pytest conventions and patterns
│   ├── 04-docs.md                    # Docstrings + mkdocs-material
│   ├── 05-lifecycle.md               # Deprecation ceremony + versioning
│   ├── 06-release.md                 # PyPI publishing + GitHub Actions
│   ├── 07-common-mistakes.md         # Python packaging anti-patterns
│   ├── 08-pre-commit.md              # Pre-commit hooks setup
│   ├── 09-cli-entry-points.md        # Adding a CLI to your package
│   ├── 10-monorepo.md                # Monorepo + namespace packages
│   └── 11-automated-release.md       # Automated version bumps + changelog
├── scripts/
│   ├── count-tokens.py               # Token budget checker
│   └── check-structure.py            # Audit project against conventions
└── .github/
    └── workflows/
        └── check-budget.yml          # CI: token budget check on PRs
```

## Token Budget

Follows [posit-dev/skills](https://github.com/posit-dev/skills) (Posit, the company behind RStudio) conventions:

- SKILL.md description: under 100 tokens
- SKILL.md body: under 5,000 tokens / 500 lines
- Reference files: loaded on demand (no hard limit)

```bash
python3 scripts/count-tokens.py .
```

## Contributing

This project is opinionated by design. If you think a convention is wrong, open an issue — but bring a reason, not just a preference. The goal is a *philosophy*, not a menu of options.
