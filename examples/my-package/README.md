# my-package

A tiny CSV reader utility.

## Installation

```bash
pip install my-package
```

## Quick start

```python
from my_package import read_csv, validate_schema

# Read a CSV file into a list of dicts
rows = read_csv("people.csv")

# Ensure required columns exist
validate_schema(rows, ["name", "age"])

print(rows[0]["name"])  # Alice
```
