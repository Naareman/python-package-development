# 04 — Documentation

R equivalent: `roxygen2` (docstrings) + `pkgdown` (website). The Python stack is
Google-style docstrings + `mkdocstrings` + `mkdocs-material`.

The principle: **documentation is written at the same time as the function, not after.**

---

## Docstring Style — Google Format, Always

```python
def read_csv(path: str | Path, encoding: str = "utf-8") -> pd.DataFrame:
    """Read a CSV file into a DataFrame.

    Args:
        path: Path to the CSV file. Can be a string or Path object.
        encoding: File encoding. Defaults to "utf-8".

    Returns:
        A DataFrame with the file contents. Column types are inferred.

    Raises:
        FileNotFoundError: If the file does not exist at the given path.
        FileFormatError: If the file cannot be parsed as CSV.

    Example:
        >>> df = read_csv("data/results.csv")
        >>> df.head()
           id  value
        0   1   10.0
        1   2   20.0
    """
```

R equivalent: roxygen2 `@param`, `@return`, `@examples`.

### Rules for docstrings

- **Every public function gets a docstring.** No exceptions.
- **First line is a one-sentence summary.** Imperative mood: "Read a CSV..." not "Reads a CSV..."
- **Args section for every parameter** — even obvious ones.
- **Returns section always** — describe the type AND what it contains.
- **Raises section** for every exception the function can raise.
- **Example section** for anything non-trivial.

### Internal functions

Internal functions (`_name`) get a shorter docstring — one line is fine if the function
is simple. But if it's complex, document it fully regardless of the underscore.

---

## mkdocs Setup

### `mkdocs.yml` (at project root, not inside `docs/`)

```yaml
site_name: my-package
site_url: https://you.github.io/my-package
repo_url: https://github.com/you/my-package

theme:
  name: material
  features:
    - navigation.tabs
    - navigation.sections
    - content.code.copy
  palette:
    - scheme: default
      primary: indigo

plugins:
  - search
  - mkdocstrings:
      handlers:
        python:
          paths: [src]
          options:
            docstring_style: google
            show_source: true
            show_root_heading: true

nav:
  - Home: index.md
  - API Reference: api.md
```

### `docs/api.md` — auto-generated from docstrings

```markdown
# API Reference

::: my_package.read_csv

::: my_package.write_csv

::: my_package.validate_schema
```

That's it. `mkdocstrings` pulls the rest from your docstrings automatically.

R equivalent: `pkgdown`'s `reference/` section auto-generated from roxygen2.

---

## README — The Front Door

The README is the first thing users see. It must answer three questions immediately:

1. **What does it do?** — one sentence
2. **How do I install it?** — one code block
3. **How do I use it?** — one real example

```markdown
# my-package

Read, validate, and transform CSV data with clear error messages.

## Installation

\`\`\`bash
pip install my-package
\`\`\`

## Quickstart

\`\`\`python
from my_package import read_csv, validate_schema

df = read_csv("data/results.csv")
validate_schema(df, schema={"required": ["id", "value"]})
\`\`\`
```

---

## Building and Previewing Docs

```bash
# Serve locally with live reload
uv run mkdocs serve

# Build static site
uv run mkdocs build

# Deploy to GitHub Pages
uv run mkdocs gh-deploy
```

---

## Documentation Checklist

Before releasing any version, verify:

- [ ] Every public function has a Google-style docstring
- [ ] Every `Raises` section lists actual exceptions from `errors.py`
- [ ] `docs/api.md` includes every public function
- [ ] README quickstart example actually runs
- [ ] CHANGELOG.md is up to date
