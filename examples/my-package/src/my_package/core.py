"""Core CSV reading and validation logic."""

from __future__ import annotations

import csv
from pathlib import Path

from my_package import _messages as msg
from my_package.errors import FileFormatError, ValidationError


def read_csv(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV file and return its rows as a list of dicts.

    Each dict maps column headers to cell values. The first row of the
    file is treated as the header row.

    Args:
        path: Path to the CSV file.

    Returns:
        A list of dictionaries, one per row.

    Raises:
        FileFormatError: If the file is empty or cannot be parsed.

    Example:
        >>> rows = read_csv("data.csv")
        >>> rows[0]["name"]
        'Alice'
    """
    filepath = Path(path)
    msg.info(f"Reading {filepath.name}")

    try:
        text = filepath.read_text(encoding="utf-8")
    except OSError as exc:
        raise FileFormatError(
            f"Cannot open file: {exc}",
            path=filepath,
        ) from exc

    if not text.strip():
        raise FileFormatError("File is empty", path=filepath)

    reader = csv.DictReader(text.splitlines())

    if reader.fieldnames is None:
        raise FileFormatError("No header row found", path=filepath)

    rows = list(reader)
    msg.success(f"Read {len(rows)} row(s) from {filepath.name}")
    return rows


def validate_schema(
    data: list[dict[str, str]],
    schema: list[str],
) -> list[dict[str, str]]:
    """Validate that every required column exists in the data.

    Checks the keys of the first row against the required column names
    in *schema*. Returns the data unchanged if validation passes.

    Args:
        data: Rows returned by :func:`read_csv`.
        schema: List of required column names.

    Returns:
        The original *data*, unmodified.

    Raises:
        ValidationError: If *data* is empty or a required column is
            missing. The ``field`` attribute names the first missing
            column.

    Example:
        >>> rows = [{"name": "Alice", "age": "30"}]
        >>> validate_schema(rows, ["name", "age"])
        [{'name': 'Alice', 'age': '30'}]
    """
    if not data:
        raise ValidationError("Data is empty", field="<all>")

    columns = set(data[0].keys())

    for field in schema:
        if field not in columns:
            raise ValidationError(
                f"Missing required column: {field}",
                field=field,
            )

    msg.success(f"Schema validated ({len(schema)} required column(s))")
    return data
