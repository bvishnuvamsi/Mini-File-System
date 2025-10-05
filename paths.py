# mini_fs/paths.py
from __future__ import annotations
from typing import List
from errors import InvalidPathError

def path_tokens(path: str) -> List[str]:
    """
    Convert an absolute UNIX-like path string into clean tokens.
    - Requires absolute paths (must start with '/').
    - Collapses multiple slashes.
    - Handles '.' (current dir) and '..' (parent) without going above root.
    - Returns [] for the root '/'.

    Examples:
    "/a//b/./c/.."   -> ["a", "b"]
    "/"              -> []
    "/../.."         -> []
    "/a/../../b"     -> ["b"]
    """
    if not isinstance(path, str) or path == "":
        raise InvalidPathError("path must be a non-empty string")
    if not path.startswith("/"):
        raise InvalidPathError("only absolute paths are supported (must start with '/')")

    tokens: List[str] = []
    for part in path.split("/"):
        if part == "" or part == ".":        # skip empty and current-dir
            continue
        if part == "..":                      # go up if possible
            if tokens:
                tokens.pop()
            # if already at root, stay at root; don't error
            continue
        # normal component
        tokens.append(part)
    return tokens


def tokens_to_path(tokens: List[str]) -> str: #Helper to pretty-print tokens back to an absolute path (for debug/tests).
    return "/" if not tokens else "/" + "/".join(tokens)