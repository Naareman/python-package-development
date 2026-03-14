"""Public exception hierarchy for my-package."""

from __future__ import annotations

from pathlib import Path


class MyPackageError(Exception):
    """Base exception for all my-package errors."""


class ValidationError(MyPackageError):
    """Raised when data fails schema validation.

    Attributes:
        field: The name of the field that failed validation.
    """

    def __init__(self, message: str, *, field: str) -> None:
        super().__init__(message)
        self.field = field


class FileFormatError(MyPackageError):
    """Raised when a file cannot be parsed as valid CSV.

    Attributes:
        path: The path to the file that caused the error.
    """

    def __init__(self, message: str, *, path: Path) -> None:
        super().__init__(message)
        self.path = path
