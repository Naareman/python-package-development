"""Internal messaging helpers (rich Console wrappers)."""

from __future__ import annotations

from rich.console import Console

_out = Console()
_err = Console(stderr=True)


def info(message: str) -> None:
    """Print an informational message to stdout."""
    _out.print(f"[bold blue]info:[/] {message}")


def success(message: str) -> None:
    """Print a success message to stdout."""
    _out.print(f"[bold green]ok:[/] {message}")


def warn(message: str) -> None:
    """Print a warning message to stderr."""
    _err.print(f"[bold yellow]warn:[/] {message}")


def abort(message: str, *, code: int = 1) -> None:
    """Print an error message to stderr and exit.

    Args:
        message: The error description.
        code: Exit code (default 1).
    """
    _err.print(f"[bold red]error:[/] {message}")
    raise SystemExit(code)
