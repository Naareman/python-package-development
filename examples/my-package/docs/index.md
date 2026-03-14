# my-package

A tiny CSV reader utility.

## Installation

```bash
pip install my-package
```

## Quick start

```python
from my_package import read_csv, validate_schema

rows = read_csv("data.csv")
validate_schema(rows, ["name", "age"])
```
