# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
