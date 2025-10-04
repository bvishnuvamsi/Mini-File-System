# mini_fs/nodes.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class Node:
    name: str
    parent: Optional["Directory"] = None  # root has parent=None

    def is_dir(self) -> bool:
        return isinstance(self, Directory)

    def is_file(self) -> bool:
        return isinstance(self, File)

    def path(self) -> str: #Return absolute path like /, /docs, /docs/notes.txt
        if self.parent is None:
            return "/"  # root
        parts = []
        cur: Optional[Node] = self
        while cur is not None and cur.parent is not None:
            parts.append(cur.name)
            cur = cur.parent
        parts.reverse()
        return "/" + "/".join(parts)


@dataclass
class Directory(Node):
    children: Dict[str, Node] = field(default_factory=dict)

    def add(self, node: Node) -> None: #Attach a child (used later by higher-level APIs).
        if node.name in self.children:
            raise ValueError(f"name already exists in directory: {node.name}")
        node.parent = self
        self.children[node.name] = node

    def remove(self, name: str) -> Node:
        node = self.children.pop(name)
        node.parent = None
        return node


@dataclass
class File(Node):
    content: str = ""
