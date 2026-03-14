"""my-package -- A tiny CSV reader utility."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("my-package")
except PackageNotFoundError:  # pragma: no cover
    __version__ = "0.0.0+dev"

from my_package.core import read_csv, validate_schema
from my_package.errors import FileFormatError, ValidationError

__all__ = [
    "FileFormatError",
    "ValidationError",
    "__version__",
    "read_csv",
    "validate_schema",
]
