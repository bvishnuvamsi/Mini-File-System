# fs.py
from __future__ import annotations
from typing import Tuple, List
import errors as E
from nodes import Node, Directory, File
from paths import path_tokens

"""
    Minimal in-memory file system wrapper around our tree.
    Provides:
      - resolve(path) -> Node
      - mkdir, rmdir
      - create_file, read_file, delete_file
"""

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
    
    def mkdir(self, path: str) -> None:
        """
        Create a single directory (no parents auto-created).
        Errors:
          - InvalidPathError if '/' (root) is requested
          - NotFoundError / NotADirectoryError if parent doesn't exist / is a file
          - AlreadyExistsError if a node already exists at that name
        """
        parent, name = self._resolve_parent_and_name(path)
        if name in parent.children:
            target = ("" if parent.path() == "/" else parent.path()) + "/" + name
            raise E.AlreadyExistsError(f"path already exists: {target}")
        parent.add(Directory(name=name))

    def rmdir(self, path: str) -> None:
        """
        Remove an empty directory.
        Errors:
          - NotFoundError if path missing
          - NotADirectoryError if target is a file
          - DirectoryNotEmptyError if directory has children
          - InvalidPathError if trying to remove root '/'
        """
        node = self.resolve(path)
        if not isinstance(node, Directory):
            raise E.NotADirectoryError(f"not a directory: {node.path()}")
        if node.parent is None:
            raise E.InvalidPathError("cannot remove root directory '/'")
        if node.children:
            raise E.DirectoryNotEmptyError(f"directory not empty: {node.path()}")
        node.parent.remove(node.name)

    def create_file(self, path: str, content: str) -> None:
        """
        Create a file at 'path' with given content.
        Errors:
          - InvalidPathError if '/' requested
          - NotFoundError / NotADirectoryError if parent missing / not a directory
          - AlreadyExistsError if name already taken (file or directory)
        """
        parent, name = self._resolve_parent_and_name(path)
        if name in parent.children:
            target = ("" if parent.path() == "/" else parent.path()) + "/" + name
            raise E.AlreadyExistsError(f"path already exists: {target}")
        parent.add(File(name=name, content=content))

    def read_file(self, path: str) -> str:
        """
        Return the content of a file.
        Errors:
          - NotFoundError if path missing
          - NotAFileError if path points to a directory
        """
        node = self.resolve(path)
        if not isinstance(node, File):
            raise E.NotAFileError(f"not a file: {node.path()}")
        return node.content

    def delete_file(self, path: str) -> None:
        """
        Delete a file.
        Errors:
          - NotFoundError if path missing
          - NotAFileError if path points to a directory
        """
        node = self.resolve(path)
        if not isinstance(node, File):
            raise E.NotAFileError(f"not a file: {node.path()}")
        # parent must exist because root is a directory
        assert node.parent is not None
        node.parent.remove(node.name)

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