# python-package-development

> *"Just as Hadley Wickham brought the Grammar of Graphics to R as ggplot2, this skill brings the philosophy of R package development to Python."*

## What is this?

**python-package-development** is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) plugin that teaches Claude how to build Python packages the right way — using the hard-won wisdom of the R package ecosystem.

**For Python developers who want their packages to feel as polished as tidyverse R packages** — whether you're creating your first library or maintaining a production package.

Python has incredible packages. But it has never had a unified philosophy for *building* them. The R world has one: Hadley Wickham's [*R Packages*](https://r-pkgs.org/) book (with Jenny Bryan), backed by tools like `devtools`, `usethis`, `roxygen2`, `cli`, and `lifecycle`.

This plugin translates that philosophy into Python using modern tools: `uv`, `rich`, `pytest`, and `mkdocs-material`.

## Installation

### Via plugin marketplace (recommended)

```
/plugin marketplace add Naareman/python-package-development
/plugin install python-package-development@python-package-development
```

### Manual install (personal scope)

```bash
git clone https://github.com/Naareman/python-package-development.git
cp -r python-package-development/skills/python-package-development \
  ~/.claude/skills/python-package-development
```

### Verify it's installed

In Claude Code, type `/python-package-development` — you should see it in the skill list.

## Examples

### Scaffold a new package from scratch

```
You:  /python-package-development scaffold my-analytics-lib
```

Claude creates the full package structure following all conventions:

```
my-analytics-lib/
├── pyproject.toml          # uv + hatchling, PEP 735 dependency-groups
├── mkdocs.yml              # mkdocs-material with mkdocstrings
├── src/
│   └── my_analytics_lib/
│       ├── __init__.py     # curated __all__, importlib.metadata version
│       ├── py.typed        # PEP 561 type marker
│       ├── errors.py       # base exception + typed errors
│       ├── _messages.py    # rich console (info, success, warn, abort)
│       └── core.py         # verb_noun() functions with Google docstrings
├── tests/
│   ├── conftest.py         # shared fixtures
│   └── test_core.py        # happy path + error cases
└── docs/
    ├── index.md
    └── api.md
```

### Review your API design

```
You:  /python-package-development api
```

Claude reads your code and checks:
- Are functions named `verb_noun()`? Are families consistent?
- Are errors in `errors.py` with a proper hierarchy?
- Is `_messages.py` used instead of bare `print()`?
- Does every public function have a Google-style docstring?

### Audit for common mistakes

```
You:  /python-package-development check
```

Claude scans your project for 30+ known anti-patterns:
- `requires-python` with an upper bound?
- Dev dependencies in `[project] dependencies`?
- `--cov=src` instead of `--cov=my_package`?
- Missing `py.typed`? `tests/__init__.py` exists?
- `license = { text = "MIT" }` (deprecated)?

### Set up pre-commit hooks

```
You:  /python-package-development pre-commit
```

Claude adds `.pre-commit-config.yaml` with ruff (lint + format), mypy, and standard hooks — no black, isort, or flake8 needed.

### Deprecate a function properly

```
You:  I need to rename parse_file() to read_csv()
```

The skill activates automatically and walks you through the deprecation ceremony:
1. Keep `parse_file()`, add `DeprecationWarning` pointing to `read_csv()`
2. Set a removal timeline in the docstring and CHANGELOG
3. Remove in the promised version

### Prepare a PyPI release

```
You:  /python-package-development release
```

Claude walks through the release ritual:
1. All tests pass? Lint clean? Types check?
2. CHANGELOG updated? Version bumped?
3. Git tag created? Tag pushed?
4. CI publishes to PyPI automatically via trusted publishing

### Just ask naturally

The skill also activates when you describe what you need:

```
You:  I want to make a Python library for parsing config files
You:  Help me structure my code as a package
You:  How should I name these functions?
You:  How do I publish to PyPI?
```

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
| Pre-commit | `lintr` + `styler` | ruff + mypy + pre-commit |
| CLI | `Rscript` | `click` / `argparse` + entry points |
| Monorepo | — | uv workspaces + namespace packages |
| Automated release | — | `bump-my-version` + `git-cliff` |

## Plugin Structure

```
python-package-development/
├── .claude-plugin/
│   ├── plugin.json                   # Plugin metadata
│   └── marketplace.json              # Marketplace catalog
├── skills/
│   └── python-package-development/
│       ├── SKILL.md                  # Main skill (philosophy + routing)
│       └── references/               # 14 reference docs (loaded on demand)
├── examples/
│   └── my-package/                   # Reference implementation (22/22 checks)
├── scripts/
│   ├── count-tokens.py               # Token budget checker
│   └── check-structure.py            # Convention audit (22 checks)
└── .github/
    └── workflows/
        └── check-budget.yml          # CI: budget + example audit on PRs
```

## Token Budget

Follows [posit-dev/skills](https://github.com/posit-dev/skills) (Posit, the company behind RStudio) conventions:

- SKILL.md description: under 100 tokens
- SKILL.md body: under 5,000 tokens / 500 lines
- Reference files: loaded on demand (no hard limit)

```bash
python3 scripts/count-tokens.py skills/python-package-development/
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). This project is opinionated by design — bring a reason, not just a preference.
