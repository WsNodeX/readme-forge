# Distribution — why a clean README is not enough

A clean README removes the reason visitors **bounce**. It does not create the
reason they **arrive**. These are different problems and only one of them is
solved by writing.

This file exists because the most common failure mode after a successful audit is
believing the work is done.

## The mechanism: GitHub Trending

GitHub Trending ranks by **star velocity over a short window**, not by total
stars. Practically:

- A repo gaining 100 stars in 24 hours trends.
- A repo gaining 1,000 stars over a year does not.

This is the single most important fact in the whole growth model. It means the
question is not "how do I get stars" but "how do I concentrate them into one
48-hour window".

`Trendshift` (trendshift.io) is a third-party service that records these windows.
Its badge on a README is not decoration — it is proof that the repo once had a
velocity spike. That is why top repos display it prominently.

## The sequence that actually works

```
1. Ship something a specific person is stuck without
        ↓
2. README that survives 30 seconds of a stranger's attention
        ↓
3. One real image (screenshot / diagram / GIF of it working)
        ↓
4. Pick a launch window — a weekday, US morning (14:00–16:00 UTC)
        ↓
5. Post in the same 2-hour window, everywhere at once
        ↓
6. Velocity spike → GitHub Trending → organic traffic
        ↓
7. Trendshift records it → badge → permanent social proof
```

Step 5 is the one people skip, and it is the only step that requires leaving the
keyboard for a platform other than GitHub.

## Where to post, ranked by realistic yield

| Channel | Yield | Notes |
|---|---|---|
| Hacker News (Show HN) | Highest variance | Front page = thousands of visitors. Post Tue–Thu, 14:00–16:00 UTC. Title must be plain and factual; hype gets flagged. |
| Reddit `r/programming`, `r/Python`, `r/java` | High, but rule-bound | Read each sub's self-promotion rules first. Most require you to be an active member, not a drive-by poster. |
| X / Twitter | Medium | Only works if you already have followers. A 0-follower account posting a link gets nothing. |
| 即刻 / V2EX / 掘金 | Medium, China-only | Good for Chinese-language projects. V2EX 分享创造 node is the highest-signal. |
| LinkedIn | Low for stars, high for jobs | Different goal. Useful if the target is an internship, not a star count. |
| Discord / Slack communities | Low volume, high quality | Best source of the first 20 real users, who then tell others. |

**Do not post to all of them at once if you have never posted before.** Post to
one, watch the response, adjust the title, then post to the next. The title is
usually what was wrong, not the project.

## What gets a Show HN flagged

- Title with adjectives: "Blazing fast..." → flagged
- Asking for upvotes anywhere → banned
- Posting the same link repeatedly → banned
- A landing page with an email gate instead of a working demo → ignored

What works: a plain title (`Show HN: A 200-line LRU cache in Python`), a first
comment that explains the tradeoff honestly, and a link that runs immediately.

## The first 20 stars

The first 20 are the hardest and they are not organic. They come from:

- People you have actually talked to
- Communities where you are a real participant
- Someone with reach who found it genuinely useful

Twenty real stars on day one can produce a trending spike. Twenty bought stars
produce nothing, because velocity is measured against a baseline of real
engagement — a spike with no forks, no issues and no traffic reads as fake.

## What not to do

- **Do not buy stars.** GitHub detects it, and a repo with 500 stars and 0 forks
  reads as fraudulent to every engineer who checks.
- **Do not create many small repos to "build a portfolio".** Twenty-five repos at
  0.5 stars each signal nothing. One repo at 50 stars signals competence. This is
  arithmetic, not opinion.
- **Do not post the same link to ten subreddits in an hour.** Automod catches it
  and the account gets shadowbanned.
- **Do not add a badge for a trending list you have not appeared on.**

## The honest summary

Distribution is a separate skill from engineering, and most engineers are bad at
it because they have never practised it. The README work in this skill is
necessary — a trending repo with a broken README converts nothing — but it is not
sufficient.

If the goal is an internship rather than a star count, the ranking is different:
a small number of well-documented, genuinely-used projects plus a clear commit
history beats a large number of starred-but-empty repos, because the person
reading is checking whether you can finish things, not whether you can market.
