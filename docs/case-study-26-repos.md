# Case study: auditing 26 repositories

A record of what happened when I pointed `readme-forge` at my own GitHub account
and fixed everything it found. Kept because the numbers are more useful than any
advice I could give, and because three of the bugs were ones no amount of reading
would have caught.

---

## Starting point

25 public repositories, all generated from a similar template. Every one had a
README, a badge or two, and a CI workflow. On inspection:

| Metric | Value |
|---|---|
| Repositories | 25 |
| Total stars | 12 |
| Forks | 0 |
| Open issues | 0 |
| GitHub Pages | 0 |
| Topics per repo | 7–10 (limit considered: 5) |
| Average README length | 8,592 characters |
| Repos with ≥1 real image | 6 / 24 |
| Repos with >3 badges | 23 / 24 |
| Repos with first code block past line 40 | 21 / 24 |

**Every repository failed the audit.** 200 violations total.

---

## What the audit found

### The dominant failure: author-facing text shipped to readers

Fourteen READMEs contained a complete Chinese blog draft — a launch plan written by
the generator for itself — as a visible section or inside an HTML comment.

```
## 六、如何把本文扩展成一篇发布稿

- **标题建议**：《我用 600 行纯 Python 手写了 PyTorch 的内核》
- **配图建议**：README 里已经有一张分层架构图
- **钩子开头**：从"你真的懂 loss.backward()"这种反问切入
- **发布平台**：适合掘金 / 知乎；B 站讲"手写框架"系列非常有受众
```

About 1,300 lines of this across the account. Moved to `docs/article-draft.md` in
each repo — the content was not worthless, it just did not belong in a document a
stranger reads to decide whether to use the code.

The line `README 里已经有一张分层架构图` was also false: that README had six image
references, all of them shields.io badges.

### The structural failure: badges as a substitute for evidence

23 of 24 repos had more than three badges, and every one of them was a hand-written
string — `badge/tests-60%20passing`, `badge/CI-passing`. Neither updated. One repo's
CI was red while its badge said passing.

Replaced with three live badges: stars, release, license.

### The layout failure: no visual asset

Six of 24 repos had a single real image. Everything else had only badges. A README
with no image asks the reader to imagine the thing working.

Every repo now carries either a Mermaid diagram or a real screenshot.

---

## The three bugs that mattered most

These are the reason this case study exists: none of them were findable by reading.

### 1. `forge` could not be imported at all

```python
>>> import forge
ModuleNotFoundError: No module named 'forge.core.registry'
```

`forge/core/registry.py` was referenced by three files and had never been written.
Consequences: the tokenizer, the trainer and the CLI all failed at import; the
37-test suite could not run; the repo could not have been used by anyone.

Its badge said `tests-passing`.

I wrote the missing module to the interface the tests expected, then verified:
`import forge` works, `load("english")` returns 255 merges, encode/decode round-trips,
and `Ran 37 tests — OK`.

### 2. `cobalt` had Windows paths stored as filenames

36 of 40 paths looked like this in the git tree:

```
cobalt\__init__.py
cobalt\policies\lru.py
```

Git stored each as a **single filename containing a backslash**, not as a directory
entry. On GitHub the repo was unbrowsable; on Windows `git clone` failed with
`invalid path`; on Linux and macOS it was unusable; CI could never have run.

Fixed by cloning with `--no-checkout`, reading every blob out of the object database
by SHA, writing each to its correctly separated path, and rebuilding the index. The
script is `readme-forge/scripts/fix_backslash_paths.py`.

Then a second bug surfaced: `tests/__init__.py` was missing, so the CI command
`python -m unittest discover -s tests` raised `Start directory is not importable`.
pytest worked because it walks directories directly, which is why nobody noticed.
With the marker added: `Ran 71 tests — OK`.

### 3. `slate` documented a failing form that reported success

The README taught this:

```python
class User(Model):
    name: Str        # type annotation
    age: Int
```

That produces a model with **no fields**. The metaclass only collects values that
are `isinstance(val, Field)`, so annotations are skipped, and `validate()` then
returns an empty model with `valid=True`.

For a validation library, silently passing invalid input is the worst possible
failure mode. The working form is `name = Str(min_len=2)`.

---

## Wrong API examples: 19 in total

Every README was executed, not merely proofread. Nineteen documented calls did not
work:

| Repo | Wrong | Right |
|---|---|---|
| `cobalt` | `cache.stats()` | `cache.stats` (a `@property`) |
| `cobalt` | `@cached(maximum_size=256)` | `@cached(cache_obj, key_fn=None)` |
| `cobalt` | `policy("tinylfu")` | only 7 policies registered; `tinylfu` is not one |
| `lumen` | `HnswIndex(m=16, ef_build=200)` | `HnswIndex(dim, M=16, ef_construction=200)` |
| `lumen` | `create_collection(..., index=...)` | `index_type=` + `index_params=` |
| `lumen` | `collection.stats` | `collection.stats()` — the opposite of `cobalt` |
| `lattice` | `MinHash.update(set)` | `update_batch(iterable)` |
| `marble` | `InMemoryLock.unlock()` | `unlock(String token)` |
| `prism` | `Prism(use_cache=True)` | `cache=SemanticCache()` — objects, not booleans |
| `prism` | `prism.use_cache().use_retry()` | `use_cache()` returns the cache, so it cannot chain |
| `prism` | `ScriptedProvider(script=["text"])` | each rule is a `dict` |
| `prism` | `@register_tool("name", "desc")` | `name=`/`description=` are keyword-only |
| `onyx` | `def get_user(request, id)` | route params live on `request.path_params` |
| `onyx` | `errorhandler(request, exc)` | `errorhandler(exc)` |
| `noesis` | `AgentConfig.defaults()` | `AgentConfig.builder()...build()` |
| `sage` | raised tool → JSON-RPC `error` | returns `result.isError: true` |
| `atlas` | a guessed `find`-based `javac` line | `src/atlas/*/*.java` |
| `forge` | `cli train corpus.txt` | `train --corpus corpus.txt` |
| `halo` | `Metrics`, `RagAnswer` as top-level | `Evaluator.Metrics`, `RagEngine.RagAnswer` |

A reader following any of these would have hit an exception. Two of them
(`cobalt.stats`, `lumen.stats`) were **opposite conventions** in sibling libraries.

---

## The audit tool was wrong six times

Each fix came from the tool failing on real data:

| Version | Findings on a healthy 13-file codebase | Problem |
|---|---|---|
| v1 | **50** | rule 6 fired on every undocumented function including `sqrt()`; rule 8 fired on private helpers mutating their own lists |
| v2 | 16 | rule 6 requires ≥2 unannotated params; rule 8 only public functions |
| v3 | 16 | rule 1 skips slice bounds, indexing, `range()`, keyword args, UPPER_CASE assigns |

And four correctness bugs:

1. `alt=` attributes were read as body text, so the tool's own hero caption failed its
   own author-facing-text rule.
2. `--json` printed the human summary to stdout after the JSON array, breaking `| jq`.
   Only visible when auditing 24 repos in bulk.
3. The local walker descended into `.pytest_cache` and audited the README pytest
   generates there.
4. Rule 3 matched the word `TODO` inside docstrings — including the docstring that
   documents rule 3, so the checker reported two findings against itself.

**Rule 4 is the same class of bug as the original problem**: a document that quotes a
bad example gets flagged for containing it. The fix — run text rules on prose only,
stripping fenced blocks, inline code and HTML attributes — is the single most
important line in the tool.

---

## Final state

| Metric | Before | After |
|---|---|---|
| Repos audited clean | 0 / 24 | **26 / 26** |
| CI green | 22 / 25 | **26 / 26** |
| Average README length | 8,592 chars | ~3,400 chars |
| Repos with a real image | 6 / 24 | 26 / 26 |
| Topics per repo | 7–10 | 5 or fewer |
| Article drafts in READMEs | 14 repos | 0 |

Two new repositories were published during this work: `readme-forge` (the audit tool)
and `inheritor` (the same principle applied to code), both with CI that runs the tool
against itself.

---

## What generalises

1. **Run the examples.** Nineteen documented calls were wrong. Reading would have
   caught none of them — they are all plausible.
2. **Local pass is not done.** Four repos passed the local audit and still failed the
   remote one, because GitHub's `topics` field does not exist in the README. Verify
   against the live API.
3. **A checker that cries wolf is worthless.** v1's 50 findings on healthy code would
   have made the tool unusable regardless of how correct its rules were. Tuning false
   positives is not polish, it is the product.
4. **Distinguish use from mention.** Every linting tool eventually meets the file that
   documents its own rules.
5. **Clean READMEs do not create demand.** All of this work raises the conversion rate
   of visitors who already arrived. It does nothing about whether anyone arrives. That
   is distribution, and it is a different job.
