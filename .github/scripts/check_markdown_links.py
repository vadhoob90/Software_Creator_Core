"""Validate local links in repository Markdown files."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote


LINK_PATTERN = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
EXTERNAL_PREFIXES = ("http://", "https://", "mailto:")
GENERATED_DIRECTORIES = {".git", ".venv", "mutants", "dist", "build", "node_modules"}


def markdown_files(root: Path) -> list[Path]:
    """Return source Markdown, excluding dependencies and generated outputs."""
    return sorted(
        path
        for path in root.rglob("*.md")
        if not GENERATED_DIRECTORIES.intersection(path.relative_to(root).parts)
    )


def local_target(source: Path, raw_target: str) -> Path | None:
    """Resolve a Markdown target when it refers to a local repository path."""
    target = raw_target.strip().strip("<>")
    if not target or target.startswith(EXTERNAL_PREFIXES) or target.startswith("#"):
        return None

    path_text = unquote(target.split("#", 1)[0].split("?", 1)[0])
    if not path_text:
        return None
    return (source.parent / path_text).resolve()


def main() -> int:
    """Report missing local Markdown link targets."""
    root = Path.cwd().resolve()
    missing: list[str] = []

    for source in markdown_files(root):
        text = source.read_text(encoding="utf-8")
        for raw_target in LINK_PATTERN.findall(text):
            target = local_target(source, raw_target)
            if target is not None and not target.exists():
                missing.append(
                    f"{source.relative_to(root)}: missing target {raw_target!r}"
                )

    if missing:
        print("\n".join(missing))
        return 1

    print("All local Markdown links resolve.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
