# README templates by project type

A README is not one genre. The reader of a library arrives with a task; the reader
of an app arrives with a suspicion; the reader of a skill arrives with no idea what
problem it solves. The same skeleton does not serve all of them.

Five templates follow, each shaped by **who arrives and what they need in the first
twenty seconds**. Every one satisfies the 13 audit rules by construction — in
particular: at most 3 live badges, at least one real image, first runnable code
within 40 lines, under 4,000 characters.

---

## How to pick

| Your project is | Use | The reader's first question |
|---|---|---|
| a library someone imports | [Library](#1-library) | "What does this replace, and can I install it in one line?" |
| a tool someone runs | [CLI](#2-cli) | "Show me the output." |
| something with a UI | [Application](#3-application) | "What does it look like, and does it actually work?" |
| an Agent Skill | [Skill](#4-agent-skill) | "What will my agent do differently after I install this?" |
| an algorithm implementation | [Teaching implementation](#5-teaching-implementation) | "Can I read this and understand the algorithm?" |

Mixed projects pick the primary one. A library with a CLI is still a library.

---

## 1. Library

The reader wants to import it. Everything else is secondary.

```markdown
<div align="center">

# <name>

### <one sentence: what it does, in plain words>

[![Stars](.../github/stars/U/R)](...) [![Release](.../github/v/release/U/R)](...) [![License](.../badge/license-MIT-111111)](...)

</div>

---

<one paragraph: what problem this solves that the obvious alternative doesn't>

## Install

```bash
<the actual one-liner>
```

## Use

```<lang>
<the smallest complete example — import, one call, printed result>
```

## What it does

<2-4 bullets, each a capability, not a feature name>

## API

| Name | What it does | Returns |
|---|---|---|
| `<fn>(<args>)` | | |

## Design notes

- <the one non-obvious decision, and why>
- <the trade-off you accepted>

## Limits

- <what it does not do>
- <what it does not handle>

## License

[MIT](LICENSE)
```

**Why this order.** Install before Use because the reader will not read your
example if they cannot run it. API table after Use because the example already
showed the common path. Limits near the bottom but above License — it is a reason
to keep reading, not a fine-print disclaimer.

**The most common failure** is a badge wall and a "Features" list of adjectives.
`Fast` · `Lightweight` · `Easy to use` carry no information. Replace each with
something measurable or delete it.

---

## 2. CLI

The reader wants to see output before they install anything.

```markdown
<div align="center">

# <name>

### <what it does, in the form of a command it runs>

[badges: ≤3, live]

</div>

---

<one line: what this replaces in your terminal>

```console
$ <name> <args>
<actual output, several lines, including the useful part>
```

## Install

```bash
<one-liner>
```

## What those flags do

| Flag | Effect |
|---|---|

## Why not just <the shell one-liner>?

<the honest comparison. If a one-liner does 80% of it, say so.>

## Limits

- <exit codes, file size, encoding — the things that bite>
```

**Why the output block comes before Install.** A CLI's value is entirely in what
it prints. If the first code block is `npm install`, the reader leaves without
knowing what the tool does. Show the output, then explain how to get it.

**Make the output real.** Copy it from an actual run. An invented example is
usually cleaner than reality, and readers notice — real output has ragged columns
and one weird line, and that is what makes it credible.

---

## 3. Application

The reader is deciding whether this is a toy. Show them it isn't.

```markdown
<div align="center">

# <name>

### <what it is for, in one sentence a non-technical person would understand>

[badges: ≤3]

</div>

![<alt text describing what the screenshot shows>](assets/screenshot.png)

<one paragraph: the problem, in the user's words, not the developer's>

## Try it

<live link — and say what state it is in: demo, alpha, self-hosted only>

## How it works

<mermaid diagram or architecture image — the data flow, not the file tree>

## Run it yourself

```bash
<minimal steps: clone, configure, run>
```

## What's not done

- <honest list. This builds more trust than any feature list.>

## License
```

**Why "What's not done" is a section, not an omission.** An application README
that claims completeness gets audited by the reader, and they will find the gaps.
Declaring them first converts a weakness into evidence of self-awareness.

**Screenshot rules.** One real screenshot beats five mockups. Crop it to what
matters. Alt text describes the content (`A form with three fields, one showing a
validation error`), not the filename.

---

## 4. Agent Skill

The reader has a client open and wants to know what changes.

```markdown
<div align="center">

# <name>

### <what your agent does differently after installing this>

[badges: ≤3]

</div>

---

<one paragraph: the failure this skill corrects. Concrete, not abstract.>

## Install

```bash
<the actual command for the most common client>
```

## What it does

| Trigger | What happens |
|---|---|
| <what the user says> | <what the skill produces> |

## Before / after

<table>
<tr><td>

**Without the skill**

```
<input> → <bad output>
```
</td><td>

**With the skill**

```
<input> → <good output>
```
</td></tr>
</table>

## How it decides

<the rules it applies — a numbered list the reader can argue with>

## Limits

- <what it won't catch>
- <when it gives a false positive>
```

**Why before/after beats a feature list.** A skill's value is a difference in
output. Showing two outputs side by side proves the difference exists; describing
it in prose asks the reader to trust you.

**The false-positive section is not optional.** Every checker of any kind produces
wrong answers. Naming the cases where yours does is the single strongest signal
that you actually ran it.

---

## 5. Teaching implementation

The reader wants to understand the algorithm. They are not going to use this in
production and both of you know it.

```markdown
<div align="center">

# <name>

### <the algorithm> in <N> lines of <language>, no dependencies

[badges: ≤3]

</div>

---

<one paragraph: what this implements and why from scratch. Say plainly that it is
for reading, not for production.>

```<lang>
<the core of the algorithm — the 20 lines that are the point>
```

## The whole thing

```
<file tree with a one-line comment per file saying what it holds>
```

## Why <the key decision>

<the one part that is genuinely subtle, explained properly. This is the section
people link to.>

## Correctness

```bash
<the command that runs the tests>
```

<N tests. List what they actually check — gradient checking, reference comparison,
edge cases.>

## What this is not

- Not optimised. <where it would be slow>
- Not complete. <which parts of the real algorithm are omitted>
- Not maintained as a library. <no semver promise>

## Further reading

- <the paper / the canonical implementation>
```

**Why "What this is not" is the longest section.** A teaching implementation gets
compared to the real thing. Pre-empting the comparison — naming exactly what was
simplified — is what makes it trustworthy as an explanation.

**The correctness section must cite real numbers.** "59 tests, including gradient
checks against finite differences at every operation" is evidence. "Well tested"
is not.

---

## Applying the audit

All five templates pass `readme-audit.py` by construction. Check anyway:

```bash
python scripts/readme-audit.py --dir path/to/repo
```

If you adapted a template and it now fails, the failure is more likely correct
than the template. Rules 1 and 2 (author-facing text, platform promotion) catch
things that leak in during drafting — a "TODO: add screenshot" left in place, a
"publishing to Hacker News next week" note that was meant for a private file.
