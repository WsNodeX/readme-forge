---
description: Audit a README and rewrite it for the reader instead of the author
argument-hint: <path/to/repo or owner/repo>
---

Load the `readme-forge` skill from `.agents/skills/readme-forge/SKILL.md` and apply it to: $ARGUMENTS

Work in this order, and do not skip step 1:

1. **Audit first.** Run `python scripts/readme-audit.py --dir <path>` for a local
   repo, or `--repo <owner/name>` for a remote one. Show me the raw output.
2. **Quote the failures.** For every issue, paste the exact offending line from
   the README. Do not paraphrase — I want to see what a stranger sees.
3. **Answer the one-line pitch.** What does this do that a competent engineer
   could not do in an afternoon? Who is stuck without it? What is the smallest
   command that proves it works? If you cannot answer the first question, stop and
   tell me the problem is the project, not the README.
4. **Rewrite** to the skeleton in the skill. Target 300–800 characters of prose.
5. **Re-audit.** It must exit 0 before you show me the result.

Hard rules while rewriting:

- Never leave author-facing text in the README — no launch plans, no headline
  options, no image briefs, no lists of where to publish.
- Never describe an asset that is not in the repo.
- Never invent a number. If a claim has no command behind it, delete the claim.
- Never pad for length.

Show me the diff at the end, not the whole file.
