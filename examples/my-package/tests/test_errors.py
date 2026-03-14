"""Tests for my_package.errors."""

from __future__ import annotations

from pathlib import Path

from my_package.errors import (
    FileFormatError,
    MyPackageError,
    ValidationError,
)


class TestErrorHierarchy:
    """All custom errors inherit from MyPackageError."""

    def test_validation_error_is_my_package_error(self) -> None:
        err = ValidationError("bad", field="col")
        assert isinstance(err, MyPackageError)
        assert isinstance(err, Exception)

    def test_file_format_error_is_my_package_error(self) -> None:
        err = FileFormatError("bad", path=Path("x.csv"))
        assert isinstance(err, MyPackageError)
        assert isinstance(err, Exception)


class TestValidationError:
    """ValidationError carries a .field attribute."""

    def test_field_attribute(self) -> None:
        err = ValidationError("Missing column", field="email")
        assert err.field == "email"
        assert str(err) == "Missing column"


class TestFileFormatError:
    """FileFormatError carries a .path attribute."""

    def test_path_attribute(self) -> None:
        p = Path("/data/broken.csv")
        err = FileFormatError("Cannot parse", path=p)
        assert err.path == p
        assert str(err) == "Cannot parse"
