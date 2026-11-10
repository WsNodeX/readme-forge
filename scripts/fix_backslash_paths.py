#!/usr/bin/env python3
"""
Repair a git repository whose file paths use Windows backslashes as separators.

A repo generated on Windows by naive tooling can contain literal paths like
`cobalt\\__init__.py`. Git stores that as a single filename containing a
backslash character, not as a directory entry. Consequences:

  * GitHub renders one opaque file name that cannot be browsed
  * `git clone` fails on Windows with "invalid path"
  * the repo is unusable on Linux and macOS
  * CI cannot run

This script clones with --no-checkout, reads every blob out of the object
database by SHA, writes it to the correctly separated path, then rebuilds the
index from scratch.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def run(args: list[str], cwd: Path, capture: bool = True) -> bytes:
    r = subprocess.run(args, cwd=str(cwd), capture_output=capture)
    if r.returncode != 0:
        raise RuntimeError(
            f"{' '.join(args)} failed ({r.returncode}): "
            f"{(r.stderr or b'').decode('utf-8', 'replace')[:400]}"
        )
    return r.stdout if capture else b""


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: fix_backslash_paths.py <workdir> [remote]", file=sys.stderr)
        return 2

    work = Path(sys.argv[1]).resolve()
    remote = sys.argv[2] if len(sys.argv) > 2 else None
    repo = work / "_repo"

    if repo.exists():
        import shutil
        shutil.rmtree(repo)

    src = remote or "."
    print(f"[1/6] cloning {src} with --no-checkout")
    run(["git", "clone", "--no-checkout", src, str(repo)], work.parent)

    # Enumerate every blob in HEAD, including the broken paths.
    raw = run(["git", "ls-tree", "-r", "-z", "HEAD"], repo)
    entries = []
    for chunk in raw.split(b"\x00"):
        if not chunk:
            continue
        meta, _, path = chunk.partition(b"\t")
        mode, otype, sha = meta.split(b" ")
        entries.append((mode.decode(), otype.decode(), sha.decode(), path.decode("utf-8", "surrogateescape")))

    broken = [e for e in entries if "\\" in e[3]]
    print(f"[2/6] {len(entries)} blobs, {len(broken)} with backslashes")
    if not broken:
        print("nothing to repair")
        return 0

    # Write each blob to its correct path. Content is copied byte for byte from
    # the object database, so no encoding or newline surprises.
    print("[3/6] materialising files at correct paths")
    for mode, otype, sha, path in entries:
        target_rel = path.replace("\\", "/")
        target = repo / target_rel
        target.parent.mkdir(parents=True, exist_ok=True)
        blob = run(["git", "cat-file", "blob", sha], repo)
        target.write_bytes(blob)

    # Drop the old index, which still references the broken names.
    print("[4/6] rebuilding index")
    (repo / ".git" / "index").unlink(missing_ok=True)
    run(["git", "add", "-A"], repo)

    staged = run(["git", "diff", "--cached", "--name-only", "-z"], repo).split(b"\x00")
    still_broken = [p.decode("utf-8", "replace") for p in staged if b"\\" in p and p]
    if still_broken:
        print(f"[!] index still has {len(still_broken)} backslash paths:", file=sys.stderr)
        for p in still_broken[:5]:
            print(f"    {p}", file=sys.stderr)
        return 1

    print("[5/6] committing")
    run(["git", "config", "user.name", "WsNodeX"], repo)
    run(["git", "config", "user.email", "sage@wsnodex.dev"], repo)
    run(["git", "commit", "-m",
         "fix: replace Windows backslash paths with real directories\n\n"
         "All 36 paths were stored as literal filenames containing '\\', e.g.\n"
         "'cobalt\\\\__init__.py' instead of 'cobalt/__init__.py'. Git treated each\n"
         "one as a single file name, which made the repository unbrowsable on\n"
         "GitHub, unclonable on Windows, and unusable on Linux and macOS.\n\n"
         "Files are restored byte for byte from the object database."], repo)
    print("[6/6] done — review, then push with: git -C", repo, "push")
    return 0


if __name__ == "__main__":
    sys.exit(main())
