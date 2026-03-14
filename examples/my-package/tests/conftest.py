"""Shared test fixtures."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture()
def sample_rows() -> list[dict[str, str]]:
    """Two-row dataset with name and age columns."""
    return [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"},
    ]


@pytest.fixture()
def csv_file(tmp_path: Path) -> Path:
    """Write a valid CSV file and return its path."""
    path = tmp_path / "data.csv"
    path.write_text("name,age\nAlice,30\nBob,25\n", encoding="utf-8")
    return path


@pytest.fixture()
def empty_file(tmp_path: Path) -> Path:
    """Write an empty file and return its path."""
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    return path
