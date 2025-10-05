# fs.py
from __future__ import annotations
from typing import Tuple, List
import errors as E
from nodes import Node, Directory, File
from paths import path_tokens

class FileSystem:
    def __init__(self) -> None:  # Root is a Directory whose parent is None and whose printed path() is "/"
        self.root = Directory(name="/", parent=None)

    # ---------- Traversal helpers ----------

    def resolve(self, path: str) -> Node:
        """
        Return the Node at 'path' if it exists. Raise:
          - E.NotFoundError if any component is missing
          - E.NotADirectoryError if a traversal step hits a File
        """
        tokens = path_tokens(path)  # [] means root
        return self._resolve_tokens(tokens)

    def _resolve_parent_and_name(self, path: str) -> Tuple[Directory, str]:
        """
        For a create/delete target (like `/a/b/file.txt`), return:
          (parent_directory_node, "file.txt")
        Raise:
          - E.InvalidPathError if path is "/" (root has no parent)
          - E.NotFoundError / E.NotADirectoryError from traversal
        """
        tokens = path_tokens(path)
        if not tokens:
            raise E.InvalidPathError("root '/' has no parent")
        parent_tokens = tokens[:-1]
        leaf_name = tokens[-1]
        parent_node = self._resolve_tokens(parent_tokens)
        if not isinstance(parent_node, Directory):  # Parent exists but is a file → cannot create under a file
            raise E.NotADirectoryError(f"parent is not a directory: {parent_node.path()}")
        return parent_node, leaf_name

    def _resolve_tokens(self, tokens: List[str]) -> Node:
        """
        Walk from root using tokens. [] returns root.
        Raises:
          - E.NotFoundError if a child name doesn't exist
          - E.NotADirectoryError if trying to descend into a File
        """
        cur: Node = self.root
        for name in tokens:
            if not isinstance(cur, Directory):
                # We tried to go "through" a file
                raise E.NotADirectoryError(f"cannot traverse through file: {cur.path()}")
            nxt = cur.children.get(name)
            if nxt is None:
                # Build a helpful missing path string
                missing_path = "/" + "/".join(self._prefix_until(cur, name))
                raise E.NotFoundError(f"path not found: {missing_path}")
            cur = nxt
        return cur

    def _prefix_until(self, cur: Node, next_name: str) -> List[str]:
        """Helper to build a readable missing-path message."""
        parts: List[str] = []
        # Climb to root collecting names, then reverse
        n: Node | None = cur
        while n is not None and n.parent is not None:
            parts.append(n.name)
            n = n.parent
        parts.reverse()
        parts.append(next_name)
        return parts