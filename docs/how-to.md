# How to use this repo every day

## Before day 1: set up your own copy

Use the template button on the repo, clone your copy, run `./scripts/seed.py` to create the labels, milestones and 30 issues, then open Claude Code and run `/today`. Prerequisites and the details (empty repo required, template rather than fork, the Actions-button alternative) are in the README's [Get your own copy](../README.md#get-your-own-copy-quick-start) section.

## TL;DR

1. `/today`: picks the next open issue and creates the entry file.
2. Read the issue's **Resources** (10–15 min).
3. `/tutor`: Claude asks the questions and you answer them (5–10 min).
4. Write the entry yourself, from memory (15 min).
5. `/polish`: fixes spelling and structure, and lists gaps as questions.
6. Explain it out loud in 2 minutes with no notes.
7. `git commit -m "<type>: <topic>" -m "Closes #N"` and `git push`.

Weeks 1–3: concepts on weekdays (#1–17). Week 4 onward: 2 concept days and 3 design days. Every week: 1 teardown day and 1 `/quiz` review day.

---

## The daily loop (30–45 min)

| Step | Time | What you do | Tool |
|---|---|---|---|
| 1. Start | 2 min | Pick the next issue and create the entry | `/today` |
| 2. Learn | 10–15 min | Read the issue's Resources and work through the Cover checklist | the resources |
| 3. Get questioned | 5–10 min | Claude asks the questions and you answer them | `/tutor` |
| 4. Write | 15 min | Fill in the template in your own words | you |
| 5. Clean up | 2 min | Fix spelling, structure and syntax | `/polish` |
| 6. Prove it | 2 min | Explain the topic out loud with no notes | you |
| 7. Ship | 1 min | Commit with `Closes #N` and push | git |

Steps 3 and 4 are where you actually learn. Reading feels productive, but you only find out what you don't understand when you have to answer questions or write it down.

On design days, add a step after writing: ask Claude to "run the design-reviewer agent on `designs/<folder>`". It critiques the entry like an interviewer would and asks follow-up questions, but it won't rewrite anything.

## Walkthrough: Day 1 (issue #01, Back-of-the-envelope estimation)

**1. Start (2 min).** Open Claude Code in the repo and type `/today`. It finds issue #01, sees the `concept` label, and suggests the slug `back-of-the-envelope-estimation`. After you confirm, it runs:

```sh
./scripts/new.sh concept back-of-the-envelope-estimation 1
```

That creates `concepts/<today>-back-of-the-envelope-estimation.md` with the date and issue number filled in, and adds a row to the README progress log. Claude then shows you the issue's checklist: powers of 2, latency numbers, QPS / storage / bandwidth math, and peak vs average load.

**2. Learn (10–15 min).** Open the two system-design-primer links in the issue (the powers-of-two table and the latency numbers), then read the Back-of-the-envelope Estimation chapter in Alex Xu's book. Don't take notes in the entry file yet. Just read, and do the arithmetic yourself. For example, work out roughly how many seconds are in a day (about 86,400, call it 10^5), because you'll use that number constantly.

**3. Get questioned (5–10 min).** Type `/tutor 1`. Claude asks one question at a time, for example:

> "A service has 100M daily active users, each making 10 requests a day. What's the average QPS?"

You answer: 10^9 requests / 10^5 seconds = 10^4 QPS.

> "Good. What would you plan capacity for, and why not that number?"

If you get stuck, it gives you a hint rather than the answer. At the end it lists what you've got solid and what's still shaky. The shaky items tell you what to focus on when you write.

**4. Write (15 min).** Close the resources and fill in the template from memory:

- **What it is:** a sentence or two in your own words.
- **Why it exists:** e.g. "So I can rule out designs that can't hit the numbers before drawing boxes."
- **How it works:** the powers-of-2 shortcuts, the few latency numbers worth memorizing (memory vs SSD vs network vs cross-region), and the QPS → peak → storage → bandwidth chain.
- **Trade-offs / when NOT to use it:** e.g. when precision matters more than order of magnitude.
- **Real-world example:** do a full estimate, such as the storage a Twitter-like service needs per year.
- **Questions I still have:** whatever the tutor exposed.

Only look things up again if you're completely blocked. The gaps you hit here are useful information.

**5. Clean up (2 min).** Type `/polish`. Claude fixes typos, moves text under the right headings and repairs markdown. It shows you a diff and won't add facts. It ends by listing gaps as questions, like "You give a peak QPS but never say what multiplier you used. Why that number?" You fill those in yourself.

**6. Prove it (2 min).** Explain the topic out loud, without notes, to a rubber duck or a voice memo. If you stall, that section of the entry needs another pass. This is one of the "Done when" checkboxes.

**7. Ship (1 min).**

```sh
git add concepts/ README.md
git commit -m "concept: back-of-the-envelope estimation" -m "Closes #1"
git push
```

When the push lands on `main`, GitHub closes issue #1. Tomorrow, `/today` will pick up #02.

## The weekly rhythm, in phases

The README sets a rhythm of 2 concept days, 3 design days, 1 teardown day and 1 review day. Issues #1–17 are all concepts, though, and the first design issue is #18. The designs also depend on the fundamentals: the URL shortener needs caching and ID generation. So the rhythm runs in phases:

- **Weeks 1–3 (#1–17):** concepts on all 5 weekday slots.
- **Week 4 onward (#18–30):** 2 concept days and 3 design days. By then most concept days are `review` revisits.
- **Teardown day (every week):** `/today teardown`. Pick an engineering blog post and open an issue for it from the teardown template (it applies the `teardown` label automatically). Then use `./scripts/new.sh teardown <slug> <issue#>`.
- **Review day (every week):** `/quiz` on past entries. Results go to `reviews/quiz-log.md`. If you score below 60%, or the same weak spot comes up twice, it offers to open a `review` issue so you revisit that entry.

## Claude's role

See `CLAUDE.md`. In short: Claude scaffolds, questions, reviews and polishes, and you write the substance. If Claude ever adds content on request, it marks it with `<!-- claude -->`.
