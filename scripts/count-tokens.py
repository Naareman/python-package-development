#!/usr/bin/env python3

"""Count tokens and lines in pyckage skill files.

Usage:
    python3 scripts/count-tokens.py [skill-dir]
    uv run scripts/count-tokens.py [skill-dir]

If no directory is given, uses the current directory.

Token estimation uses word-based heuristic (~1.3 tokens per word).
For exact counts, install tiktoken: pip install tiktoken

Limits (following posit-dev/skills conventions):
    - SKILL.md description: 100 tokens
    - SKILL.md body: 5,000 tokens / 500 lines
    - Reference files: no hard limit (reported only)
"""

import re
import sys
from pathlib import Path


# Limits
DESC_TOKEN_LIMIT = 100
SKILL_TOKEN_LIMIT = 5_000
SKILL_LINE_LIMIT = 500

# Try tiktoken for exact counts, fall back to word-based estimate
_encoder = None
try:
    import tiktoken
    _encoder = tiktoken.get_encoding("cl100k_base")
except ImportError:
    pass


def count_tokens(text: str) -> int:
    """Count tokens using tiktoken if available, else estimate from words."""
    if _encoder is not None:
        return len(_encoder.encode(text))
    # Rough heuristic: ~1.3 tokens per whitespace-separated word
    words = len(text.split())
    return int(words * 1.3)


def parse_frontmatter(content: str) -> tuple[dict[str, str], str]:
    """Split YAML frontmatter from markdown body."""
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)", content, re.DOTALL)
    if not match:
        return {}, content

    fm_text = match.group(1)
    body = match.group(2)

    attrs: dict[str, str] = {}
    current_key: str | None = None
    current_val: list[str] = []

    for line in fm_text.split("\n"):
        key_match = re.match(r"^(\w[\w-]*):\s*(.*)", line)
        if key_match:
            if current_key:
                attrs[current_key] = " ".join(current_val).strip()
            current_key = key_match.group(1)
            val = key_match.group(2).strip()
            if val == ">":
                current_val = []
            else:
                current_val = [val]
        elif current_key and line.startswith("  "):
            current_val.append(line.strip())

    if current_key:
        attrs[current_key] = " ".join(current_val).strip()

    return attrs, body


def main() -> None:
    skill_dir = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
    skill_md = skill_dir / "SKILL.md"

    if not skill_md.exists():
        print(f"Error: {skill_md} not found")
        sys.exit(1)

    method = "tiktoken" if _encoder else "estimate (~1.3x words)"

    content = skill_md.read_text()
    attrs, body = parse_frontmatter(content)

    skill_name = attrs.get("name", skill_dir.name)
    description = attrs.get("description", "")

    # Collect files
    files = [skill_md]
    refs_dir = skill_dir / "references"
    if refs_dir.is_dir():
        files.extend(sorted(refs_dir.glob("*.md")))

    scripts_dir = skill_dir / "scripts"
    if scripts_dir.is_dir():
        files.extend(sorted(scripts_dir.glob("*.py")))

    # Header
    print(f"\n  skill token budget: {skill_name}")
    print(f"  Method: {method}")
    print(f"  {'=' * 64}")

    # Description check
    desc_tokens = count_tokens(description)
    desc_warn = " !!!" if desc_tokens > DESC_TOKEN_LIMIT else ""
    print(f"\n  Description: {desc_tokens} tokens (limit: {DESC_TOKEN_LIMIT}){desc_warn}")

    # File table
    print(f"\n  {'File':<40} {'Lines':>6} {'Tokens':>8}  Status")
    print(f"  {'-' * 40} {'-' * 6} {'-' * 8}  {'-' * 10}")

    total_lines = 0
    total_tokens = 0

    for f in files:
        text = f.read_text()
        lines = text.count("\n")
        tokens = count_tokens(text)
        total_lines += lines
        total_tokens += tokens

        rel = f.relative_to(skill_dir)
        warnings = []

        if f == skill_md:
            body_lines = body.count("\n")
            body_tokens = count_tokens(body)
            if body_tokens > SKILL_TOKEN_LIMIT:
                warnings.append(f"body {body_tokens} > {SKILL_TOKEN_LIMIT} tokens")
            if body_lines > SKILL_LINE_LIMIT:
                warnings.append(f"body {body_lines} > {SKILL_LINE_LIMIT} lines")

        status = ", ".join(warnings) if warnings else "ok"
        print(f"  {str(rel):<40} {lines:>6} {tokens:>8}  {status}")

    print(f"  {'-' * 40} {'-' * 6} {'-' * 8}")
    print(f"  {'TOTAL':<40} {total_lines:>6} {total_tokens:>8}")
    print()

    # Summary
    has_warnings = desc_tokens > DESC_TOKEN_LIMIT
    body_tokens = count_tokens(body)
    body_lines = body.count("\n")
    if body_tokens > SKILL_TOKEN_LIMIT or body_lines > SKILL_LINE_LIMIT:
        has_warnings = True

    if has_warnings:
        print("  !!! Budget exceeded — consider moving content to references/")
    else:
        print("  All within budget.")
    print()


if __name__ == "__main__":
    main()
