#!/usr/bin/env python3
"""
readme-audit — 13-point README audit.

Rules are defined in .agents/skills/readme-forge/SKILL.md and mirrored here so
the skill's advice is machine-checkable rather than aspirational.

Usage:
    python scripts/readme-audit.py --dir path/to/repo
    python scripts/readme-audit.py --repo WsNodeX/ember
    python scripts/readme-audit.py --repo a/b,c/d --json
    python scripts/readme-audit.py --dir . --strict    # warnings also fail

Exit codes: 0 = pass, 1 = violations found.

Requires only the Python standard library.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

# ── thresholds ────────────────────────────────────────────────────────────
MAX_BADGES = 3
MIN_REAL_IMAGES = 1
MAX_CHARS = 4000
GOOD_CHARS = 800
MAX_TOPICS = 5
FIRST_CODE_MAX_LINE = 40

# Tooling directories contain generated READMEs (pytest writes one) that are not
# the project's own documentation and must never be audited.
EXCLUDE_DIRS = {
    ".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
    "node_modules", ".venv", "venv", "env", "site-packages", "dist", "build",
    ".next", "target", "vendor",
}

# ── rule 1/2/8: author-facing text and reader address ─────────────────────
AUTHOR_FACING = [
    (r"如何把本文", "author-facing: 'how to expand this article'"),
    (r"发布稿", "author-facing: 'launch post'"),
    (r"标题建议", "author-facing: 'headline options'"),
    (r"配图建议", "author-facing: 'image brief'"),
    (r"钩子开头", "author-facing: 'hook suggestion'"),
    (r"发布平台", "author-facing: 'publishing platforms'"),
    (r"扩展成一篇", "author-facing: 'expand into an article'"),
    (r"headline (options|suggestions?)", "author-facing: 'headline options'"),
    (r"image brief", "author-facing: 'image brief'"),
    (r"launch post", "author-facing: 'launch post'"),
    (r"publishing platform", "author-facing: 'publishing platforms'"),
    (r"how to expand this (article|into)", "author-facing: 'article expansion plan'"),
]

PLATFORM_PROMO = [
    (r"掘金", "platform promotion: 掘金"),
    (r"知乎", "platform promotion: 知乎"),
    (r"公众号", "platform promotion: 公众号"),
    (r"B站|bilibili", "platform promotion: B站"),
    (r"小红书", "platform promotion: 小红书"),
    (r"dev\.to", "platform promotion: dev.to"),
    (r"hacker news|\bHN\b", "platform promotion: Hacker News"),
    (r"r/Python|r/programming", "platform promotion: Reddit"),
]

READER_ADDRESS = [
    (r"读者朋友", "reader address: 读者朋友"),
    (r"话不多说", "reader address: 话不多说"),
    (r"让我们开始", "reader address: 让我们开始"),
    (r"今天我们来", "reader address: 今天我们来"),
    (r"let'?s dive in", "reader address: \"let's dive in\""),
    (r"buckle up", "reader address: 'buckle up'"),
    (r"without further ado", "reader address: 'without further ado'"),
]

# unfalsifiable marketing words — rule 4 in the skill's hard rules
SLOP_WORDS = [
    r"production[- ]ready", r"battle[- ]tested", r"enterprise[- ]grade",
    r"blazing(ly)?[- ]fast", r"seamless(ly)?", r"powerful",
    r"robust", r"cutting[- ]edge", r"state[- ]of[- ]the[- ]art",
]

BADGE_HOSTS = ("shields.io", "badgen.net", "badge.fury.io")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)")
HTML_IMG_RE = re.compile(r"<img[^>]+src=[\"']([^\"']+)[\"']")
MERMAID_RE = re.compile(r"^```mermaid", re.MULTILINE)
TOPICS_RE = re.compile(r"^(topics|tags)\s*:", re.MULTILINE | re.IGNORECASE)

FENCED_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
HTML_TAG_RE = re.compile(r"<[^>]+>")


def prose_only(text: str) -> str:
    """
    Reduce a README to the words a reader actually reads, before text rules run.

    Three things get stripped:
      * fenced code blocks — a README documenting a bad example must quote it
      * inline code        — `dev.to` in backticks is a citation, not promotion
      * HTML tags          — this removes alt="" and srcset= attributes; an image
                             alt describing "headline options" is a caption, not
                             author-facing body text

    Without the third rule, this project's own hero image alt text would fail
    its own audit. Telling use from mention is the hardest part of the job.
    """
    no_fences = FENCED_RE.sub("", text)
    no_inline = INLINE_CODE_RE.sub("", no_fences)
    return HTML_TAG_RE.sub("", no_inline)


# ── fetching ──────────────────────────────────────────────────────────────
def gh_headers(raw: bool = True) -> dict:
    h = {
        "User-Agent": "readme-audit",
        "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    tok = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return h


def fetch(url: str, raw: bool = True) -> str:
    req = urllib.request.Request(url, headers=gh_headers(raw))
    with urllib.request.urlopen(req, timeout=25) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_remote(repo: str) -> tuple[str, str, int | None]:
    """Return (repo, readme_text, topic_count). API first — raw is unreachable
    on some networks even when api.github.com works."""
    errors = []
    try:
        text = fetch(f"https://api.github.com/repos/{repo}/readme")
        topics = None
        try:
            meta = json.loads(fetch(f"https://api.github.com/repos/{repo}", raw=False))
            topics = len(meta.get("topics") or [])
        except Exception:
            pass
        return repo, text, topics
    except Exception as e:
        errors.append(f"api: {e}")
    for branch in ("main", "master"):
        try:
            text = fetch(f"https://raw.githubusercontent.com/{repo}/{branch}/README.md")
            return repo, text, None
        except Exception as e:
            errors.append(f"raw/{branch}: {e}")
    raise RuntimeError("; ".join(errors))


# ── analysis ──────────────────────────────────────────────────────────────
def first_code_line(text: str) -> int | None:
    """1-based line number of the first fenced code block."""
    for i, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            return i
    return None


def analyze(name: str, text: str, base_dir: Path | None, topics: int | None) -> dict:
    issues: list[str] = []
    warns: list[str] = []

    # Text rules run on prose only — quoted examples are citations, not usage.
    prose = prose_only(text)

    def hit(patterns, bucket):
        for pat, label in patterns:
            m = re.search(pat, prose, re.IGNORECASE)
            if m:
                bucket.append(f"{label} (matched 「{m.group(0)}」)")

    # rules 1, 2, 8
    hit(AUTHOR_FACING, issues)
    hit(PLATFORM_PROMO, issues)
    hit(READER_ADDRESS, issues)

    # rule 4: slop adjectives -> warning, not failure (they are pervasive)
    slop = [w for w in SLOP_WORDS if re.search(w, prose, re.IGNORECASE)]
    if slop:
        warns.append(f"unfalsifiable adjectives: {', '.join(slop[:4])}")

    # rules 3, 5: badges vs real images. Mermaid blocks count as real images.
    mermaid = len(MERMAID_RE.findall(text))
    imgs = IMG_RE.findall(text) + HTML_IMG_RE.findall(text)
    badges = [u for u in imgs if any(h in u for h in BADGE_HOSTS)]
    real = [u for u in imgs if u not in badges]
    real_total = len(real) + mermaid

    if len(badges) > MAX_BADGES:
        issues.append(f"{len(badges)} badges, limit is {MAX_BADGES}")
    if real_total < MIN_REAL_IMAGES:
        detail = f"{len(badges)} badges and nothing else" if badges else "no images at all"
        issues.append(f"zero real images ({detail}) — no diagram, screenshot, chart or GIF")
    if mermaid:
        warns.append(f"{mermaid} Mermaid block(s) counted as real images")

    # rule 4b: are badges live data or hand-written strings?
    live = [u for u in badges if re.search(r"/(github|npm|pypi|crates)/|/v/|/stars/|/downloads/", u)]
    if badges and not live:
        warns.append(f"all {len(badges)} badges are static strings, none show live data")

    # rule 6: phantom assets
    if base_dir is not None:
        for u in real:
            if u.startswith(("http://", "https://", "data:")):
                continue
            if not (base_dir / u.lstrip("./")).exists():
                issues.append(f"phantom asset: {u} is referenced but not in the repo")
    if re.search(r"(已经?有|包含|附有|reuse the|already (has|includes)).{0,24}"
                 r"(架构图|示意图|流程图|截图|diagram|screenshot|chart)", prose, re.IGNORECASE):
        if real_total == 0:
            issues.append("claims a diagram/screenshot that does not exist")

    # rule 7: unwitnessed numbers
    for m in re.finditer(r"(\d[\d,.]*)\s*(?:unit\s+)?tests?\s+passing", prose, re.IGNORECASE):
        if base_dir is not None:
            count = 0
            for p in base_dir.rglob("test*.py"):
                if ".git" in p.parts:
                    continue
                try:
                    count += len(re.findall(r"^\s*def test_", p.read_text(encoding="utf-8", errors="ignore"), re.M))
                except Exception:
                    pass
            if count and abs(count - int(m.group(1).replace(",", ""))) > max(2, count * 0.2):
                issues.append(
                    f"unwitnessed number: claims {m.group(1)} tests, repo has {count} test functions"
                )
        else:
            warns.append(f"test count '{m.group(0)}' cannot be verified remotely")

    # rule 9: length
    chars = len(text)
    if chars > MAX_CHARS:
        issues.append(f"{chars:,} characters, limit is {MAX_CHARS:,} — padding, not depth")
    elif chars > GOOD_CHARS:
        warns.append(f"{chars:,} characters, target is {GOOD_CHARS}")

    # rule 10: time to first code
    fcl = first_code_line(text)
    if fcl is None:
        warns.append("no code block at all — reader cannot see it work")
    elif fcl > FIRST_CODE_MAX_LINE:
        issues.append(f"first code block on line {fcl}, limit is {FIRST_CODE_MAX_LINE}")

    # rule 13: topics
    if topics is not None and topics > MAX_TOPICS:
        issues.append(f"{topics} topics, limit is {MAX_TOPICS}")

    return {
        "name": name,
        "chars": chars,
        "badges": len(badges),
        "images": real_total,
        "first_code_line": fcl,
        "issues": issues,
        "warns": warns,
    }


def walk_local(root: Path) -> list[tuple[str, str, Path | None, int | None]]:
    out = []
    seen: set[Path] = set()
    # rglob is case-insensitive on Windows, so 'readme.md' and 'README.md' both
    # match the same file — dedupe on the resolved path.
    candidates = list(root.rglob("[Rr][Ee][Aa][Dd][Mm][Ee].[Mm][Dd]"))
    for p in sorted(candidates):
        if EXCLUDE_DIRS & set(p.parts):
            continue
        rp = p.resolve()
        if rp in seen:
            continue
        seen.add(rp)
        try:
            out.append((str(p.relative_to(root)), p.read_text(encoding="utf-8"), p.parent, None))
        except UnicodeDecodeError:
            continue
    return out


# ── entry ─────────────────────────────────────────────────────────────────
def main() -> int:
    ap = argparse.ArgumentParser(description="13-point README audit")
    ap.add_argument("--dir", help="scan a local directory")
    ap.add_argument("--repo", help="scan a remote repo, comma separated")
    ap.add_argument("--strict", action="store_true", help="warnings also fail")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args()

    targets: list[tuple[str, str, Path | None, int | None]] = []
    if args.repo:
        for r in [x.strip() for x in args.repo.split(",") if x.strip()]:
            try:
                name_, text_, topics_ = fetch_remote(r)
                targets.append((name_, text_, None, topics_))
            except Exception as e:
                print(f"[ERR] {r}: {e}", file=sys.stderr)
    else:
        targets = walk_local(Path(args.dir or ".").resolve())

    if not targets:
        print("[ERR] no README.md found", file=sys.stderr)
        return 1

    results = [analyze(n, t, b, tp) for n, t, b, tp in targets]

    if args.json:
        # Nothing else may be printed in this mode — a summary line on stdout
        # breaks `| jq` and ConvertFrom-Json, which is the whole point of --json.
        print(json.dumps(results, ensure_ascii=False, indent=2))
        failed = [r for r in results if r["issues"]]
        warned = [r for r in results if r["warns"] and not r["issues"]]
        if failed:
            return 1
        if args.strict and warned:
            return 1
        return 0

    print(f"{'repo/file':<30} {'chars':>6} {'badge':>5} {'img':>4} {'code@':>6}  verdict")
    print("-" * 74)
    for r in results:
        verdict = "FAIL" if r["issues"] else ("WARN" if r["warns"] else "PASS")
        fcl = r["first_code_line"] if r["first_code_line"] is not None else "-"
        print(f"{r['name'][:29]:<30} {r['chars']:>6} {r['badges']:>5} "
              f"{r['images']:>4} {str(fcl):>6}  {verdict}")
        for i in r["issues"]:
            print(f"    x {i}")
        for w in r["warns"]:
            print(f"    ! {w}")

    failed = [r for r in results if r["issues"]]
    warned = [r for r in results if r["warns"] and not r["issues"]]
    passed = len(results) - len(failed) - len(warned)

    print()
    print(f"{len(results)} audited · {len(failed)} fail · {len(warned)} warn · {passed} pass")

    # Topics live in the GitHub repo settings, not in the README. A local audit
    # can report PASS on a repo that still fails remotely, which happened twice
    # during the field test. Say so rather than letting the user assume done.
    if not args.repo:
        print()
        print("note: local mode cannot check GitHub topics (limit 5).")
        print("      Run with --repo OWNER/NAME against the pushed repo before")
        print("      calling it done — a README-only fix is not the whole check.")

    if failed:
        return 1
    if args.strict and warned:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
