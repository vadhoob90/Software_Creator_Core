"""Bounded, workspace-relative reads and content hashes for context and evidence."""

import hashlib
import json
from pathlib import Path, PurePosixPath
from typing import Any

from .errors import CoreError

MAX_FILE_BYTES = 256_000


def digest(value: Any) -> str:
    """Hash canonical JSON, independent of dictionary insertion order."""
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
    return hashlib.sha256(encoded.encode()).hexdigest()


def read_artifact(root: Path, name: str) -> bytes:
    """Read an explicitly named regular file; refuse escapes, links and oversized inputs."""
    parts = PurePosixPath(name).parts
    if not parts or name.startswith("/") or "\\" in name or ".." in parts:
        raise CoreError(
            "unsafe-path",
            "Expected a workspace-relative file path.",
            "Use a regular file inside the declared workspace.",
        )
    path = root
    for part in parts:
        path = path / part
        if path.is_symlink():
            raise CoreError(
                "unsafe-path",
                "Symbolic links are not valid evidence sources.",
                "Select an ordinary workspace file.",
            )
    if not path.is_file():
        raise CoreError(
            "missing-artifact",
            "A declared artifact is not a regular file.",
            "Create the required artifact before submitting evidence.",
        )
    with path.open("rb") as stream:
        content = stream.read(MAX_FILE_BYTES + 1)
    if len(content) > MAX_FILE_BYTES:
        raise CoreError(
            "input-limit",
            "An artifact exceeds the size limit.",
            "Provide a focused artifact under 256 KB.",
        )
    return content


def file_digest(root: Path, name: str) -> str:
    return hashlib.sha256(read_artifact(root, name)).hexdigest()
