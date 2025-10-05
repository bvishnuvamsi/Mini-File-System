from __future__ import annotations
from typing import Tuple, List
import errors as E
from nodes import Node, Directory, File
from paths import path_tokens
import os  

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
    
        # ---------- Pretty tree printer ----------

    def tree_str(self) -> str:
        """Return a pretty string of the current filesystem tree."""
        lines: list[str] = []

        def _walk(node, indent: int = 0) -> None:
            spacer = "  " * indent
            if isinstance(node, Directory):
                name = "/" if node.parent is None else node.name + "/"
                lines.append(f"{spacer}{name}")
                # stable, sorted order for predictable output
                for child_name in sorted(node.children.keys()):
                    _walk(node.children[child_name], indent + 1)
            else:
                lines.append(f"{spacer}{node.name}")

        _walk(self.root)
        return "\n".join(lines)

    def tree(self) -> None:
        """Print the current filesystem tree."""
        print(self.tree_str())

    def export_to_real_fs(self, dest_root: str) -> None:
        """
        Create real folders/files under dest_root that mirror the in-memory tree.
        Safe to run inside your repo. If dest_root exists, it will be merged into.
        """
        def _walk(node, cur_path):
            from nodes import Directory, File  # local import to avoid cycle in editors
            if isinstance(node, Directory):
                os.makedirs(cur_path, exist_ok=True)
                # deterministic order
                for name in sorted(node.children.keys()):
                    _walk(node.children[name], os.path.join(cur_path, name))
            else:  # File
                os.makedirs(os.path.dirname(cur_path), exist_ok=True)
                with open(cur_path, "w", encoding="utf-8") as f:
                    f.write(node.content)

        os.makedirs(dest_root, exist_ok=True)
        _walk(self.root, dest_root)