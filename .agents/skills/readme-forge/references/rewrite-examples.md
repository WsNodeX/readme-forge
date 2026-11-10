# Rewrite examples — before and after

Each pair is a real failure shape found in AI-generated READMEs.

---

## 1. The launch plan left inside the README

### Before

```markdown
## 六、如何把本文扩展成一篇发布稿

- **标题建议**：《我用 600 行纯 Python 手写了 PyTorch 的内核》
- **配图建议**：Ember 的 README 里已经有一张分层架构图
- **钩子开头**：从"你真的懂 loss.backward()"这种反问切入
- **发布平台**：适合掘金 / 知乎；B 站讲"手写框架"系列非常有受众
```

### What is wrong

Three separate failures in four lines:

1. Author-facing text in a reader-facing document
2. A claimed asset ("已经有一张分层架构图") that does not exist in the repo
3. A list of publishing platforms, which is a marketing decision, not documentation

### After

Deleted entirely. This content belongs in a separate `LAUNCH.md` that the user
asks for explicitly — never in the README.

**Rule of thumb: if deleting a paragraph loses nothing for a reader who will
never publish this project, delete it.**

---

## 2. The badge wall replacing evidence

### Before

```markdown
![Python](https://img.shields.io/badge/python-3.9%2B-3776AB?logo=python)
![License: MIT](https://img.shields.io/badge/license-MIT-green)
![Dependencies](https://img.shields.io/badge/dependencies-0-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS-lightgrey)
![Tests](https://img.shields.io/badge/tests-60%20passing-brightgreen)
![Pure Python](https://img.shields.io/badge/implementation-pure%20Python-orange)
```

Six badges, zero images, and the "60 passing" is a hand-written string — it stays
green whether or not the tests pass.

### After

```markdown
<p align="center">
  <img src="https://img.shields.io/github/stars/USER/REPO?style=flat-square&color=111111&label=stars">
  <img src="https://img.shields.io/github/v/release/USER/REPO?style=flat-square&color=111111&label=release">
  <img src="https://img.shields.io/badge/license-MIT-111111?style=flat-square">
</p>

<p align="center">
  <img src="assets/demo.gif" width="720" alt="Training a linear model, loss falling to zero">
</p>
```

Three badges that update themselves, plus one image that shows the thing working.
The GIF replaces all six badges as evidence, because it cannot lie.

---

## 3. The feature-list tagline

### Before

> A zero-dependency Python toolkit of high-quality cache eviction policies:
> FIFO, LRU, LFU, LRU-K, SLRU, ARC, TinyLFU, W-TinyLFU.

### After

> An LRU cache in 200 lines, with the benchmarks to prove it beats `functools.lru_cache`.

**Why it works:** the first version answers "what features exist". The second
answers "why should I install this instead of the one I already have". A reader
who needs an LRU cache already has one; you have to beat it, not list at it.

Cost: the second version is falsifiable. If the benchmark is not there, the
sentence is a lie. That is the point — a falsifiable claim is a reason to trust
the rest.

---

## 4. The unwitnessed number

### Before

> Tested with 60 unit tests, every operation validated against central
> finite-difference gradients.

### Problem

Where is 60? Run `grep -rc "def test_" tests/ | awk -F: '{s+=$2} END {print s}'`.
If the answer is 34, the number is a lie, and every other number in the README
becomes suspect.

### After

> ```bash
> pytest -q
> # 34 passed in 1.2s
> ```

The number now has a command in front of it. A reader who doubts it can verify
it in five seconds, which is exactly why they will not bother.

**Rule: a number without its command is a liability. Delete the number, not the
sentence around it** — deleting the number and keeping the claim is worse than
useless, because the evidence has been removed while the assertion survives.

---

## 5. The honest limitations section

This is the one section AI-written READMEs almost never include, and the one
that buys the most credibility.

### Before

> This framework is production-ready and scales to handle enterprise workloads.

### After

> **Limitations**
>
> - Pure Python: ~50x slower than the NumPy version on matrices above 512×512.
>   Fine for learning, wrong for training.
> - No GPU support, and none planned.
> - Not thread-safe; the whole engine assumes a single writer.

Stating what the project cannot do is the cheapest available signal that the
author actually built it. Anyone can claim it works; only someone who ran it
knows where it breaks.

Corollary: never write a limitation you have not measured. "Might be slow for
large inputs" is noise. "50x slower above 512×512" is information.

---

## 6. Time to first code

### Before

Lines 1–60: logo, 6 badges, table of contents, "Why Ember?", three paragraphs of
motivation, an ASCII architecture diagram. First code block on line 81.

### After

Line 1–20: name, one sentence, one image. Line 22: `## Quick start`.
Line 24: the first code block, with its output shown.

A reader deciding whether to stay has about 30 seconds. Spend none of them on
motivation — motivation is what the working demo produces in the reader, not
what a paragraph installs.
