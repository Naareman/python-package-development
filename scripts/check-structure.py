#!/usr/bin/env python3
"""Audit a Python package project against pyckage conventions."""

from __future__ import annotations

import ast
import re
import sys
from pathlib import Path


def find_package_dir(src: Path) -> Path | None:
    """Find the first package directory under src/."""
    if not src.is_dir():
        return None
    for child in sorted(src.iterdir()):
        if child.is_dir() and (child / "__init__.py").exists():
            return child
    return None


def check_init_has_all(init_path: Path) -> bool:
    """Check whether __init__.py defines __all__."""
    try:
        tree = ast.parse(init_path.read_text(encoding="utf-8"))
    except (SyntaxError, OSError):
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    return True
        if isinstance(node, ast.AnnAssign):
            if isinstance(node.target, ast.Name) and node.target.id == "__all__":
                return True
    return False


def check_pyproject(path: Path) -> list[tuple[str, bool, str]]:
    """Run pyproject.toml checks. Returns list of (name, passed, message)."""
    results: list[tuple[str, bool, str]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        results.append(("pyproject.toml readable", False, "Cannot read pyproject.toml"))
        return results

    # Use tomllib (3.11+) or fallback to regex-based checks
    try:
        import tomllib  # type: ignore[import-not-found]
        data = tomllib.loads(text)
    except ImportError:
        # Python 3.10 fallback: try tomli, else regex
        try:
            import tomli as tomllib  # type: ignore[import-not-found,no-redef]
            data = tomllib.loads(text)
        except ImportError:
            data = None

    if data is not None:
        # [build-system] exists
        results.append((
            "[build-system] table exists",
            "build-system" in data,
            "pyproject.toml has [build-system]" if "build-system" in data
            else "Missing [build-system] table in pyproject.toml",
        ))

        # license is a string (not a table)
        project = data.get("project", {})
        lic = project.get("license")
        if lic is None:
            results.append(("license is a string", False, "No license field in [project]"))
        elif isinstance(lic, str):
            results.append(("license is a string", True, f"license = \"{lic}\""))
        else:
            results.append(("license is a string", False,
                            "license should be a string (e.g. \"MIT\"), not a table"))

        # requires-python has no upper bound
        req_py = project.get("requires-python", "")
        has_upper = bool(re.search(r"<|<=", req_py))
        results.append((
            "requires-python has no upper bound",
            not has_upper,
            f"requires-python = \"{req_py}\"" if not has_upper
            else f"requires-python has upper bound: \"{req_py}\"",
        ))

        # [dependency-groups] exists (not [tool.uv.dev-dependencies])
        has_dep_groups = "dependency-groups" in data
        tool_uv = data.get("tool", {}).get("uv", {})
        has_old_dev = "dev-dependencies" in tool_uv
        if has_dep_groups and not has_old_dev:
            results.append(("dependency-groups (not uv dev-deps)", True,
                            "Uses [dependency-groups]"))
        elif has_old_dev:
            results.append(("dependency-groups (not uv dev-deps)", False,
                            "Uses [tool.uv.dev-dependencies] instead of [dependency-groups]"))
        else:
            results.append(("dependency-groups (not uv dev-deps)", False,
                            "Missing [dependency-groups] table"))

        # No target-version in [tool.ruff]
        ruff = data.get("tool", {}).get("ruff", {})
        has_tv = "target-version" in ruff
        results.append((
            "No target-version in [tool.ruff]",
            not has_tv,
            "No target-version in [tool.ruff]" if not has_tv
            else "Remove target-version from [tool.ruff] (use requires-python instead)",
        ))
    else:
        # Regex fallback for Python 3.10 without tomli
        results.append((
            "[build-system] table exists",
            bool(re.search(r"^\[build-system\]", text, re.MULTILINE)),
            "pyproject.toml has [build-system]" if re.search(r"^\[build-system\]", text, re.MULTILINE)
            else "Missing [build-system] table",
        ))

        lic_match = re.search(r'^license\s*=\s*(.+)', text, re.MULTILINE)
        if lic_match:
            val = lic_match.group(1).strip()
            is_string = val.startswith('"') or val.startswith("'")
            results.append(("license is a string", is_string,
                            f"license = {val}" if is_string
                            else "license should be a string, not a table"))
        else:
            results.append(("license is a string", False, "No license field found"))

        req_match = re.search(r'^requires-python\s*=\s*"([^"]*)"', text, re.MULTILINE)
        if req_match:
            req_py = req_match.group(1)
            has_upper = bool(re.search(r"<|<=", req_py))
            results.append(("requires-python has no upper bound", not has_upper,
                            f"requires-python = \"{req_py}\""))
        else:
            results.append(("requires-python has no upper bound", False,
                            "No requires-python found"))

        has_dg = bool(re.search(r"^\[dependency-groups", text, re.MULTILINE))
        has_old = bool(re.search(r"^\[tool\.uv\.dev-dependencies\]", text, re.MULTILINE))
        if has_dg and not has_old:
            results.append(("dependency-groups (not uv dev-deps)", True,
                            "Uses [dependency-groups]"))
        elif has_old:
            results.append(("dependency-groups (not uv dev-deps)", False,
                            "Uses [tool.uv.dev-dependencies]"))
        else:
            results.append(("dependency-groups (not uv dev-deps)", False,
                            "Missing [dependency-groups]"))

        in_ruff = False
        has_tv = False
        for line in text.splitlines():
            if re.match(r"^\[tool\.ruff\]", line):
                in_ruff = True
            elif re.match(r"^\[", line):
                in_ruff = False
            elif in_ruff and line.strip().startswith("target-version"):
                has_tv = True
        results.append(("No target-version in [tool.ruff]", not has_tv,
                        "No target-version in [tool.ruff]" if not has_tv
                        else "Remove target-version from [tool.ruff]"))

    return results


def find_bare_prints(src_dir: Path) -> list[str]:
    """Find bare print() calls in src/ Python files. Returns list of locations."""
    hits: list[str] = []
    for py_file in src_dir.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.Expr)
                and isinstance(node.value, ast.Call)
                and isinstance(node.value.func, ast.Name)
                and node.value.func.id == "print"
            ):
                hits.append(f"{py_file}:{node.lineno}")
    return hits


def check_public_docstrings(src_dir: Path) -> list[str]:
    """Check that all public functions/methods in src/ have docstrings."""
    missing: list[str] = []
    for py_file in src_dir.rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text(encoding="utf-8"), filename=str(py_file))
        except (SyntaxError, OSError):
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name.startswith("_"):
                    continue
                docstring = ast.get_docstring(node)
                if not docstring:
                    missing.append(f"{py_file}:{node.lineno} {node.name}()")
    return missing


def main() -> int:
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    root = root.resolve()

    if not root.is_dir():
        print(f"Error: {root} is not a directory")
        return 1

    results: list[tuple[str, bool, str]] = []

    # --- Structure checks ---

    src = root / "src"
    results.append((
        "src/ layout exists",
        src.is_dir(),
        "src/ directory found" if src.is_dir() else "Missing src/ directory",
    ))

    pkg_dir = find_package_dir(src)
    if pkg_dir:
        pkg_name = pkg_dir.name
        results.append(("Package directory under src/", True, f"Found src/{pkg_name}/"))
    else:
        pkg_name = "?"
        results.append(("Package directory under src/", False,
                        "No package directory with __init__.py found under src/"))

    init_path = pkg_dir / "__init__.py" if pkg_dir else src / "__init__.py"
    if init_path.exists():
        has_all = check_init_has_all(init_path)
        results.append(("__init__.py has __all__", has_all,
                        "__all__ defined in __init__.py" if has_all
                        else "__all__ not defined in __init__.py"))
    else:
        results.append(("__init__.py has __all__", False, "__init__.py not found"))

    if pkg_dir:
        py_typed = pkg_dir / "py.typed"
        results.append(("py.typed marker exists", py_typed.exists(),
                        "py.typed found" if py_typed.exists()
                        else f"Missing {pkg_name}/py.typed"))

        errors_py = pkg_dir / "errors.py"
        bad_errors = pkg_dir / "_errors.py"
        if errors_py.exists():
            results.append(("errors.py exists (not _errors.py)", True, "errors.py found"))
        elif bad_errors.exists():
            results.append(("errors.py exists (not _errors.py)", False,
                            "Found _errors.py — rename to errors.py"))
        else:
            results.append(("errors.py exists (not _errors.py)", False, "Missing errors.py"))

        messages_py = pkg_dir / "_messages.py"
        results.append(("_messages.py exists", messages_py.exists(),
                        "_messages.py found" if messages_py.exists()
                        else "Missing _messages.py"))
    else:
        results.append(("py.typed marker exists", False, "Cannot check (no package dir)"))
        results.append(("errors.py exists (not _errors.py)", False, "Cannot check (no package dir)"))
        results.append(("_messages.py exists", False, "Cannot check (no package dir)"))

    tests_dir = root / "tests"
    results.append(("tests/ directory exists", tests_dir.is_dir(),
                    "tests/ found" if tests_dir.is_dir() else "Missing tests/"))

    tests_init = tests_dir / "__init__.py"
    if tests_dir.is_dir():
        results.append(("tests/ has no __init__.py", not tests_init.exists(),
                        "No __init__.py in tests/ (good)" if not tests_init.exists()
                        else "Remove __init__.py from tests/"))
    else:
        results.append(("tests/ has no __init__.py", False, "Cannot check (no tests/ dir)"))

    conftest = tests_dir / "conftest.py"
    results.append(("conftest.py in tests/", conftest.exists(),
                    "tests/conftest.py found" if conftest.exists()
                    else "Missing tests/conftest.py"))

    mkdocs_root = root / "mkdocs.yml"
    mkdocs_docs = root / "docs" / "mkdocs.yml"
    if mkdocs_root.exists() and not mkdocs_docs.exists():
        results.append(("mkdocs.yml at project root", True, "mkdocs.yml at root"))
    elif mkdocs_docs.exists():
        results.append(("mkdocs.yml at project root", False,
                        "mkdocs.yml is inside docs/ — move to project root"))
    else:
        results.append(("mkdocs.yml at project root", False, "Missing mkdocs.yml"))

    for fname in (".python-version", ".gitignore", "CHANGELOG.md", "README.md", "pyproject.toml"):
        fpath = root / fname
        results.append((f"{fname} exists", fpath.exists(),
                        f"{fname} found" if fpath.exists() else f"Missing {fname}"))

    # --- pyproject.toml checks ---

    pyproject_path = root / "pyproject.toml"
    if pyproject_path.exists():
        results.extend(check_pyproject(pyproject_path))

    # --- Code quality checks ---

    if src.is_dir():
        prints = find_bare_prints(src)
        if prints:
            detail = f"Found {len(prints)} bare print() call(s): " + ", ".join(prints[:5])
            if len(prints) > 5:
                detail += f" ... and {len(prints) - 5} more"
            results.append(("No bare print() in src/", False, detail))
        else:
            results.append(("No bare print() in src/", True, "No bare print() calls in src/"))

        missing_docs = check_public_docstrings(src)
        if missing_docs:
            detail = f"{len(missing_docs)} public function(s) missing docstrings: " + ", ".join(
                missing_docs[:5]
            )
            if len(missing_docs) > 5:
                detail += f" ... and {len(missing_docs) - 5} more"
            results.append(("All public functions have docstrings", False, detail))
        else:
            results.append(("All public functions have docstrings", True,
                            "All public functions have docstrings"))

    # --- Output ---

    passed = sum(1 for _, ok, _ in results if ok)
    total = len(results)

    print(f"\nAuditing: {root}\n")
    for name, ok, msg in results:
        mark = "\u2713" if ok else "\u2717"
        print(f"  {mark}  {name}")
        if not ok:
            print(f"     {msg}")

    print(f"\n{passed}/{total} checks passed\n")

    return 0 if passed == total else 1


if __name__ == "__main__":
    raise SystemExit(main())
