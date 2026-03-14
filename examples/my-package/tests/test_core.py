"""Tests for my_package.core."""

from __future__ import annotations

from pathlib import Path

import pytest

from my_package.core import read_csv, validate_schema
from my_package.errors import FileFormatError, ValidationError


# -- read_csv -----------------------------------------------------------------


class TestReadCsv:
    """Tests for read_csv()."""

    def test_reads_valid_csv(self, csv_file: Path) -> None:
        rows = read_csv(csv_file)
        assert len(rows) == 2
        assert rows[0]["name"] == "Alice"
        assert rows[1]["age"] == "25"

    def test_raises_on_empty_file(self, empty_file: Path) -> None:
        with pytest.raises(FileFormatError, match="empty") as exc_info:
            read_csv(empty_file)
        assert exc_info.value.path == empty_file

    def test_raises_on_missing_file(self, tmp_path: Path) -> None:
        missing = tmp_path / "no_such_file.csv"
        with pytest.raises(FileFormatError, match="Cannot open") as exc_info:
            read_csv(missing)
        assert exc_info.value.path == missing

    def test_returns_list_of_dicts(self, csv_file: Path) -> None:
        rows = read_csv(csv_file)
        assert isinstance(rows, list)
        assert all(isinstance(r, dict) for r in rows)


# -- validate_schema ----------------------------------------------------------


class TestValidateSchema:
    """Tests for validate_schema()."""

    def test_passes_when_all_columns_present(
        self, sample_rows: list[dict[str, str]]
    ) -> None:
        result = validate_schema(sample_rows, ["name", "age"])
        assert result is sample_rows

    def test_raises_on_missing_column(
        self, sample_rows: list[dict[str, str]]
    ) -> None:
        with pytest.raises(ValidationError, match="email") as exc_info:
            validate_schema(sample_rows, ["name", "email"])
        assert exc_info.value.field == "email"

    def test_raises_on_empty_data(self) -> None:
        with pytest.raises(ValidationError, match="empty") as exc_info:
            validate_schema([], ["name"])
        assert exc_info.value.field == "<all>"

    def test_accepts_empty_schema(
        self, sample_rows: list[dict[str, str]]
    ) -> None:
        result = validate_schema(sample_rows, [])
        assert result is sample_rows
