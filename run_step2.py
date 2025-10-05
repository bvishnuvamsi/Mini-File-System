# run_demo_step2.py
from paths import path_tokens, tokens_to_path
from errors import InvalidPathError

cases = [
    "/",
    "/a",
    "/a/b",
    "/a//b/./c/..",
    "/../..",
    "/a/../../b",
]

print("Path normalization demo:")
for p in cases:
    toks = path_tokens(p)
    print(f"{p!r} -> tokens={toks} -> {tokens_to_path(toks)!r}")

print("\nError demo (relative path should fail):")
try:
    path_tokens("docs/notes.txt")
except InvalidPathError as e:
    print("Raised InvalidPathError as expected:", e)