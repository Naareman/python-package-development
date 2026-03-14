# pyckage

> *"Just as Hadley Wickham brought the Grammar of Graphics to R as ggplot2, pyckage brings the philosophy of R package development to Python."*

## What is pyckage?

**pyckage** is a [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill that teaches Claude how to build Python packages the right way — using the hard-won wisdom of the R package ecosystem.

Python has incredible packages. But it has never had a unified philosophy for *building* them. The R world has one: Hadley Wickham's [*R Packages*](https://r-pkgs.org/) book (with Jenny Bryan), backed by tools like `devtools`, `usethis`, `roxygen2`, `cli`, and `lifecycle`.

pyckage translates that philosophy into Python using modern tools: `uv`, `rich`, `pytest`, and `mkdocs-material`.

## Installation

### For all your projects (personal scope)

```bash
# Clone the repo
git clone https://github.com/Naareman/pyckage.git

# Copy to your Claude skills directory
cp -r pyckage ~/.claude/skills/pyckage
```

### For a single project (project scope)

```bash
# From your project root
mkdir -p .claude/skills
cp -r /path/to/pyckage .claude/skills/pyckage
```

### Verify it's installed

In Claude Code, run `/pyckage` — you should see it in the skill list.

## Usage

pyckage activates automatically when you're working on Python package tasks. You can also invoke it explicitly:

```
/pyckage scaffold my-new-package    # Create a new package from scratch
/pyckage api                        # Review and improve your API design
/pyckage test                       # Set up or improve tests
/pyckage docs                       # Set up mkdocs + docstrings
/pyckage lifecycle                  # Manage deprecations and versioning
/pyckage release                    # Walk through the PyPI release ritual
/pyckage check                      # Audit your project for common mistakes
/pyckage                            # Assess your project against all 5 principles
```

Or just describe what you need — pyckage will activate when it recognizes a Python packaging task:

- *"I want to make a Python library"*
- *"Help me structure my code as a package"*
- *"How should I name these functions?"*
- *"How do I publish to PyPI?"*

## The Philosophy (what R taught us)

### 1. User communication is a first-class concern
R's `cli` package made it easy to produce beautiful, structured messages. **pyckage** brings this to Python through `rich` and structured exception hierarchies.

### 2. Function names form a grammar
Tidyverse packages use `verb_noun()` consistently. Users can *guess* function names because the grammar is predictable. **pyckage** encodes naming conventions that make your API feel intentional.

### 3. Lifecycle deserves ceremony
R's `lifecycle` package gave deprecations a formal process. Users are never surprised. **pyckage** brings the same discipline to Python's `warnings` system.

### 4. Documentation lives next to code
`roxygen2` made it impossible to forget documentation. **pyckage** enforces Google-style docstrings + `mkdocstrings` so docs are always a byproduct of writing good code.

### 5. There is a whole game
Before diving into details, you should be able to see the whole thing working end-to-end. **pyckage** gives you a complete, working package skeleton from the first command.

## What pyckage Covers

| Stage | R equivalent | Python (pyckage) |
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
pyckage/
├── SKILL.md                          # Main skill definition (philosophy + routing)
├── README.md                         # This file
├── references/
│   ├── 01-scaffold.md                # Package scaffolding (the "whole game")
│   ├── 02-api-design.md              # Naming, messages, errors
│   ├── 03-testing.md                 # pytest conventions and patterns
│   ├── 04-docs.md                    # Docstrings + mkdocs-material
│   ├── 05-lifecycle.md               # Deprecation ceremony + versioning
│   ├── 06-release.md                 # PyPI publishing + GitHub Actions
│   └── 07-common-mistakes.md         # Python packaging anti-patterns
└── scripts/
    └── count-tokens.py               # Token budget checker
```

## Token Budget

pyckage follows [posit-dev/skills](https://github.com/posit-dev/skills) conventions for skill size:

- SKILL.md description: under 100 tokens
- SKILL.md body: under 5,000 tokens / 500 lines
- Reference files: loaded on demand (no hard limit)

Check with:
```bash
python3 scripts/count-tokens.py .
# Install tiktoken for exact counts: pip install tiktoken
```

## Contributing

This project is opinionated by design. If you think a convention is wrong, open an issue — but bring a reason, not just a preference. The goal is a *philosophy*, not a menu of options.
