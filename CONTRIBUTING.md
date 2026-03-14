# Contributing

This project is opinionated by design. Contributions are welcome, but please understand the philosophy before proposing changes.

## Principles

1. **Bring a reason, not a preference.** Every convention in this skill exists for a reason — usually learned from R's package ecosystem. If you want to change one, explain why the current approach causes problems.

2. **Consistency over individual taste.** We'd rather be consistently good than inconsistently perfect.

3. **Modern Python only.** We target Python 3.10+ with modern tools (uv, ruff, hatchling). Don't propose backward-compatible alternatives for older setups.

## How to contribute

### Reporting issues
- Open an issue describing what's wrong and why
- Include which reference file is affected (e.g., `references/01-scaffold.md`)
- If it's a technical inaccuracy, link to official docs that contradict us

### Proposing changes
1. Fork the repo
2. Make your changes
3. Run the token budget checker: `python3 scripts/count-tokens.py skills/python-package-development/`
4. Ensure SKILL.md stays under 500 lines / 5,000 tokens
5. Open a PR with a clear description of *why* the change improves the skill

### Adding a new reference file
- Follow the naming pattern: `NN-topic.md` (next number in sequence)
- Keep under 150 lines
- Include R equivalents where applicable
- Add a row to the reference table in SKILL.md
- Add a subcommand to the argument routing table if appropriate

### Testing
- If you change the example package, run: `python3 scripts/check-structure.py examples/my-package/`
- All 22 checks should pass

## What we won't accept

- "Add support for setuptools/poetry/flit" — we're opinionated about hatchling + uv
- Removing R equivalents — the R-to-Python mapping is a core feature
- Making the skill less opinionated — the whole point is to have opinions
