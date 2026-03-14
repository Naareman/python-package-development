# 09 — CLI Entry Points

R equivalent: writing an `Rscript`-based CLI, or using packages like `optparse` / `argparse`.
The goal is to let users run your package from the command line, not just import it.

---

## When Does a Package Need a CLI?

Not every package does. Add a CLI when users need to:

- Run a pipeline or transformation from the terminal
- Use your tool in shell scripts or CI
- Provide a standalone command (like `ruff`, `pytest`, `uv`)

If your package is purely a library (imported by other code), skip the CLI.

---

## Entry Points in pyproject.toml

```toml
[project.scripts]
my-tool = "my_package.cli:main"
```

This tells the build backend: "when this package is installed, create a `my-tool` command
that calls `main()` in `src/my_package/cli.py`." The command is placed on `PATH`
automatically — no manual symlinking.

R equivalent: there isn't one. R packages don't install commands onto `PATH`. This is
a genuine advantage of Python packaging.

---

## Simple Approach: argparse (stdlib)

No dependencies. Good enough for simple CLIs.

```python
# src/my_package/cli.py
"""Command-line interface for my-package."""
from __future__ import annotations

import argparse
import sys

from my_package import process_data


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="my-tool",
        description="Process data files.",
    )
    parser.add_argument("input", help="Path to input file")
    parser.add_argument("-o", "--output", help="Path to output file")
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args(argv)

    result = process_data(args.input, output=args.output)
    if args.verbose:
        print(f"Processed {result.n_rows} rows")


if __name__ == "__main__":
    main()
```

The `argv` parameter lets tests call `main(["input.csv", "-v"])` without subprocess.

---

## Recommended Approach: click

For anything beyond a single command, use [click](https://click.palletsprojects.com/):

```python
# src/my_package/cli.py
"""Command-line interface for my-package."""
from __future__ import annotations

import click

from my_package import process_data
from my_package._messages import info, success


@click.group()
@click.version_option()
def main() -> None:
    """My-package: process data files."""


@main.command()
@click.argument("input_path", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="Output file path.")
@click.option("-v", "--verbose", is_flag=True)
def process(input_path: str, output: str | None, verbose: bool) -> None:
    """Process a data file."""
    result = process_data(input_path, output=output)
    if verbose:
        info(f"Processed {result.n_rows} rows")
    success("Done.")
```

Add click to your dependencies (not dev — it ships with your package):

```toml
dependencies = [
    "rich>=13.0",
    "click>=8.1",
]
```

**typer** is an alternative that uses type hints instead of decorators. It depends on
click internally and adds rich output. Good choice if you prefer that style.

---

## Integrating with _messages.py

Your CLI should use the same messaging layer as the rest of the package:

```python
# In cli.py
from my_package._messages import info, warn, success, abort

@main.command()
def validate(input_path: str) -> None:
    """Validate a data file."""
    try:
        result = validate_data(input_path)
        success(f"Valid: {result.n_rows} rows, {result.n_cols} columns")
    except ValidationError as e:
        abort(str(e))  # prints error and exits with code 1
```

This gives you consistent, rich-formatted output across library and CLI usage.

---

## Testing CLI Commands

### With click: CliRunner (no subprocess, fast)

```python
from click.testing import CliRunner
from my_package.cli import main


def test_process_command(tmp_csv):
    runner = CliRunner()
    result = runner.invoke(main, ["process", str(tmp_csv)])

    assert result.exit_code == 0
    assert "Done" in result.output


def test_process_missing_file():
    runner = CliRunner()
    result = runner.invoke(main, ["process", "nonexistent.csv"])

    assert result.exit_code != 0
```

### With argparse: call main() directly

```python
from my_package.cli import main


def test_process(tmp_csv, capsys):
    main([str(tmp_csv), "--verbose"])

    captured = capsys.readouterr()
    assert "Processed" in captured.out
```

### As a last resort: subprocess

```python
import subprocess

def test_cli_installed():
    result = subprocess.run(["my-tool", "--help"], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Process data" in result.stdout
```

Use this only to verify the entry point itself is installed. All logic testing should
use the in-process approaches above.

---

## Checklist

1. Entry point defined in `[project.scripts]`
2. `main()` function is importable and testable (accepts `argv` or uses click)
3. CLI uses `_messages.py` for output, not raw `print()`
4. At least one test per command using CliRunner or direct call
5. `--help` works and describes every command
6. `--version` works (use `click.version_option()` or print `__version__`)
