# Audit rules — machine-checkable reference

Every rule here is implemented in `scripts/readme-audit.py`. This file documents
*why* each threshold exists, so the numbers can be argued with instead of obeyed.

## Severity model

**Fail** — the README actively damages the project. Fix before publishing.
**Warn** — a smell. Fix if cheap, ignore if the project genuinely needs it.

## Fail rules

### 1. Author-facing text

Patterns: `如何把本文` · `发布稿` · `标题建议` · `配图建议` · `钩子开头` ·
`发布平台` · `扩展成一篇` · `headline options` · `image brief` · `launch post` ·
`publishing platform` · `how to expand this into`

Why fail and not warn: this text is not merely useless to a reader, it is
actively harmful. It tells the reader the document was produced by a process
that never had them in mind. Trust is gone at that point; no later section
recovers it.

### 2. Platform promotion

Patterns: `掘金` · `知乎` · `公众号` · `B站` · `小红书` · `dev.to` ·
`Hacker News` · `r/Python` · `r/programming`

Same reason as rule 1. Where to publish an article is an author decision that
belongs in a separate plan file.

### 3. Badge economy — limit 3

Badges are decoration. A reader learns nothing from `badge/dependencies-0`.
Three is the point past which the reader stops reading them and starts seeing a
wall.

Sub-check (warn, not fail): if every badge is a hand-written string and none
shows live data, the wall is also useless. Prefer
`img.shields.io/github/stars/USER/REPO`, `/github/v/release/`, `/npm/v/PKG`.

### 4. Zero real images

`<img>` and `![]()` targets whose host is not a badge service, plus
` ```mermaid ` blocks, which GitHub renders natively.

Why this is a fail and not a warn: a README with no image asks the reader to
imagine the thing working. A README with one screenshot lets them see it.
The conversion difference is not subtle.

Mermaid is accepted because it needs no binary asset, renders in GitHub, and is
diffable in review — a real diagram with none of the drawbacks.

### 5. Phantom assets

Two checks:

- every local image path must exist on disk
- if the prose says a diagram/screenshot exists ("reuse the architecture diagram
  above", "already includes a chart") and there are zero real images, fail

This is the highest-value rule in the set. A model describing an asset it never
created is a specific, mechanically detectable failure mode, and it appears in
otherwise competent output.

### 6. Unwitnessed numbers

For `N tests passing`, count `def test_` in the repo. Allow 20% drift (or 2,
whichever is larger) before flagging.

Only the test-count case is automated, because it is the one with a reliable
witness. Benchmarks and user counts cannot be verified without running the
project, so they are left to human review — see `rewrite-examples.md`.

### 7. Length — 4,000 characters

Warn above 800, fail above 4,000.

The 800 target is prose, excluding code blocks. The 4,000 fail line exists
because past that point a README is usually padding a thin project rather than
documenting a thick one. If a project genuinely needs 4,000+ characters, it
probably needs a `docs/` directory instead.

### 8. Time to first code — line 40

The first fenced block must appear by line 40. A reader who has scrolled past
two screens without seeing anything runnable has no evidence the project works.

READMEs that legitimately fail this: design-document repos, awesome-lists,
curated indexes. Those projects have no runnable artifact, and the audit will
flag them anyway — treat that as a signal that the repo is a different kind of
thing, not that the README is wrong.

## Warn rules

### 9. Reader address

`读者朋友` · `话不多说` · `让我们开始` · `今天我们来` · `let's dive in` ·
`buckle up` · `without further ado`

Warn rather than fail because it is a style issue, not a credibility issue.
But it is always deletable — every one of these phrases can be removed without
losing information.

### 10. Unfalsifiable adjectives

`production-ready` · `battle-tested` · `enterprise-grade` · `blazingly fast` ·
`seamless` · `powerful` · `robust` · `cutting-edge` · `state-of-the-art`

Warn because they are pervasive and sometimes appear in quoted material.
The fix is always deletion — there is no rewrite that makes these claims true.

### 11. Feature-list taglines

Not automated (natural language). Detection: the subtitle is a comma-separated
enumeration of features rather than one sentence about who this is for.

`FIFO, LRU, LFU, LRU-K, SLRU, ARC, TinyLFU` — enumeration, fails.
`The cache library that refuses to grow` — hook, passes.

### 12. Topic stuffing — limit 5

Automated only in remote mode, via the GitHub API `topics` field.

Topics are search surface, not description. Ten topics means the author is
guessing at queries rather than stating what the project does. GitHub's own
search weights topic accuracy through engagement, so stuffing is
self-defeating — but it also looks desperate, which is the real cost.

## Why use-vs-mention matters

The single hardest problem in building this audit: a README documenting a bad
example must quote it. If quoted text counts as a violation, then the most
honest possible writeup — one that shows the failure — gets flagged.

Solution: text rules run on `prose_only(text)`, which strips fenced code blocks,
inline code, and HTML tags (removing `alt=` and `srcset=` attributes) before
matching.

Consequence: `dev.to` inside backticks is a citation and passes. `dev.to` in a
sentence fails. This is the correct behavior, and this project's own README is
the regression test for it.
