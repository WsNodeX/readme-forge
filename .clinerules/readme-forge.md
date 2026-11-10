# readme-forge

Applies to README.md files. Audit before rewriting, then verify.

## Run the audit first

```
python scripts/readme-audit.py --dir .
```

## Hard rules

Never leave in a README:

- author-facing text: launch plans, headline options, image briefs, platform lists
- unfalsifiable adjectives: production-ready, battle-tested, blazingly fast,
  seamless, powerful, robust
- numbers with no command behind them
- descriptions of images that are not in the repo

Always enforce:

- at most 3 badges, prefer live data over static strings
- at least 1 real image or Mermaid block
- first runnable code within 40 lines
- prose 300-800 characters, whole file under 4,000
- one copy-pasteable command that proves it works

## Skeleton

`# Name` → one sentence → one image → `## Install` → `## Quick start` (with real
output) → `## Why this exists` → `## API` → `## License`

## Verify

The audit must exit 0 before the rewrite counts as done.
