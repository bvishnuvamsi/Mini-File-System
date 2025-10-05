# Mini-File-System

*As a part of Week-4 assignment for the Coding Bootcamp by Cybersecurity Professionals led by Karan Dwivedi sir.*

This project is a tiny in-memory file system that supports 5 basic filesystem operations and an interactive command-line interface (CLI). Paths are absolute (starting with `/`) and path resolution is implemented manually, with no reliance on `os.path` or the real filesystem by default.

---

## Features

The five required operations are:

-   **Create Directory:** `mkdir(path)`
-   **Delete Directory:** `rmdir(path)` (only if the directory is empty)
-   **Create File:** `create_file(path, content)`
-   **Read File:** `read_file(path)` (returns content)
-   **Delete File:** `delete_file(path)`

**Note:**
-   Everything lives in memory. Use `Show tree` to inspect the current state.
-   Use `Export` to mirror the in-memory tree to your real disk (optional).

---

## Rules and Behavior

-   Paths are UNIX-like and absolute (e.g., `/docs/notes.txt`).
-   Names inside a directory must be unique.
-   Directories can contain files and other directories.
-   Deleting a directory requires it to be empty.

### Path Normalization Rules:
-   Collapse multiple slashes (`/a//b` → `/a/b`)
-   Ignore current directory references (`/a/./b` → `/a/b`)
-   Parent directory references stay within the root (`/a/..` → `/`)

---

## Command-Line Interface (CLI)

Interact with the file system via a simple menu.

### Example Session:

```bash
Mini File System — pick an option:
  1) Create directory
  2) Delete directory
  3) Create file
  4) Read file
  5) Delete file
  6) Show tree
  7) Export to real folder
  0) Exit
> 1
Directory path to create (absolute, e.g. /docs): /docs
/
  docs/
> 3
File path to create: /docs/notes.txt
Enter file content. Finish with a single line containing 'EOF':
hello world
EOF
OK: created file.
/
  docs/
    notes.txt
> 4
File path to read: /docs/notes.txt

----- file content start -----
hello world
-----  file content end  -----

> 6
/
  docs/
    notes.txt
```
---

## Implementation Details

* **Data Model (in-memory tree)**
    * A `Directory` holds a dictionary of its children (mapping names to `Node` objects).
    * A `File` holds its content as a string.
    * Each `Node` (File or Directory) stores a reference to its parent and can compute its absolute path.

* **Path Parser**
    * `path_tokens(path)` converts absolute path strings into a clean list of tokens.
    * It handles `//`, `.`, and `..` (ensuring it never escapes the root).

* **Traversal Helpers**
    * Safely resolve tokens from the root directory with clear, custom error handling (e.g., `NotFoundError`, `NotADirectoryError`).

* **Operations Layer**
    * Contains the core logic for `mkdir`, `rmdir`, `create_file`, `read_file`, and `delete_file`.

* **Tree Printer**
    * `tree()` / `tree_str()` produce a deterministic (sorted) string representation of the filesystem structure.

* **CLI**
    * A menu-driven interface with friendly error messages to interact with the filesystem.

* **Export (optional)**
    * `export_to_real_fs(dest_root)` mirrors the in-memory tree to a real folder on the disk.

---

## Repository Structure
```bash
├── cli.py              # Interactive CLI
├── errors.py           # Custom exceptions
├── fs.py               # FileSystem: traversal + 5 ops + tree printer + export
├── nodes.py            # Data model: Node, Directory, File
├── paths.py            # Path normalization logic
├── run_step2.py        # (demo) Path parsing examples
├── run_step3.py        # (demo) Traversal helpers demo
├── run_step4.py        # (demo) Five operations demo
├── run_step5.py        # (demo) Tree printer demo
└── run_export_demo.py  # (demo) Export to real folder
```
---

## How to Run

**Requirements**: Python 3.8+. No third-party libraries are needed.

1.  **Run the interactive CLI:**
    ```bash
    python3 cli.py
    ```

2.  **Export to real disk (optional) from inside the CLI:**
    * Select option `7) Export to real folder`.
    * When prompted, enter a destination folder (e.g. `out_fs`).
    * Open the exported folder (e.g., on macOS):
    ```bash
    open out_fs
    ```

---

## Constraints & Assumptions

* Only **absolute paths** (starting with `/`) are supported for simplicity.
* The system is entirely **in-memory**; no real disk writes occur unless you explicitly export.
* Deleting directories requires them to be **empty**.
* The tree print output is **alphabetically sorted** for consistency.

---

## Common Errors Handled

The CLI handles the following custom exceptions gracefully:

* `InvalidPathError` — Bad or unsupported path (e.g., `..` from root).
* `NotFoundError` — A component of the path is missing.
* `AlreadyExistsError` — Name clash on a create operation.
* `NotADirectoryError` — Attempted to traverse “through” a file (e.g., `/file.txt/other`).
* `NotAFileError` — Tried to read or delete a directory as if it were a file.
* `DirectoryNotEmptyError` — Attempted to remove a non-empty directory.

---

## Quick Demos (Optional)

You can run individual demo scripts to see specific components in action.

```bash
# Path parsing
python3 run_step2.py

# Traversal helpers
python3 run_step3.py

# Five operations
python3 run_step4.py

# Tree printer
python3 run_step5.py

# Export demo
python3 run_export_demo.py
```
