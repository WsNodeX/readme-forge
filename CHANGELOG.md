# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- `--json` mode printed the human summary line to stdout after the JSON payload,
  which broke `| jq` and PowerShell's `ConvertFrom-Json`. Found while auditing 24
  real repos in bulk — the failure only appears at scale.
- The local walker descended into tooling directories and audited generated
  files. `pytest` writes a `.pytest_cache/README.md`, which was reported as a
  failing project README. Now skips `.pytest_cache`, `__pycache__`, `node_modules`,
  `.venv`, `dist`, `build`, `target`, `vendor` and similar.

### Verified in the field

Audited 24 real repositories with this tool, then fixed four of them end to end:

| Repo | Failures before | After | What it was |
|---|---|---|---|
| `WsNodeX/ember` | 15 | 0 | A launch plan shipped inside the README, a diagram claimed but never drawn, 6 static badges, first code on line 81 |
| `WsNodeX/cairn` | 2 | 0 | 4,794 characters, first code on line 48, 3 static badges |
| `WsNodeX/vellum` | 2 | 0 | 4 static badges, zero real images |
| `WsNodeX/meter` | 1 | 0 | 4 static badges |

All 24 repos failed the audit on first pass — 200 violations total, average 8,592
characters, only 6 of 24 had a single real image, 23 of 24 had more than 3 badges.

**A trap worth recording:** all four repaired repos passed the local audit
(`--dir`) and still failed the remote one (`--repo`). The remote mode also checks
the GitHub `topics` field, which does not exist in the README, so no amount of
local editing can satisfy it. Each repo carried 7–10 topics against a limit of 5.
Local PASS is not the whole story; verify against the remote API before calling a
repo done.

### Field-test artifacts

Each repaired repo was also given its first tag and release, because the live
`/github/v/release` badge renders as "no releases" without one — a badge that
reports a failure is worse than the static string it replaced.

## [1.0.0] — 2026-11-10

### Added

- `SKILL.md` with the 13-point audit rule set and the rewrite skeleton.
- `scripts/readme-audit.py` — stdlib-only CLI, `--dir` for local repos and
  `--repo` for remote ones, `--json` for machine consumption, `--strict` to make
  warnings fail.
- `prose_only()` preprocessing that strips fenced code blocks, inline code and
  HTML attributes before text rules run. Without it, any README documenting a
  bad example would fail its own audit — including this one.
- Five client integrations: Claude Code (plugin + slash command), Codex, Cursor,
  Cline, Gemini CLI.
- Hero image and dual-theme wordmark as SVG, so they diff in review and need no
  binary tooling.
- `references/audit-rules.md` — why each threshold exists, so it can be argued with.
- `references/rewrite-examples.md` — six before/after pairs from real failures.
- `references/distribution.md` — the star-growth mechanism, and why a clean
  README is necessary but not sufficient.
- CI that runs the project's own README through its own audit on every push.

### Fixed during development

- Audit read `alt=` attributes as body text, so this project's own hero image
  caption ("headline options...") failed the author-facing-text rule.
- Remote and local targets returned tuples of different lengths.
- `rglob("README.md")` matched the same file twice on case-insensitive
  filesystems.
- Mermaid blocks were not counted as real images, which contradicted the skill's
  own advice to use them.

[Unreleased]: https://github.com/WsNodeX/readme-forge/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/WsNodeX/readme-forge/releases/tag/v1.0.0
