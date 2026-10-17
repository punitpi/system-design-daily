# Bootstrap prompt

If you just want this repo for your own practice, you don't need this prompt: click **Use this template** on GitHub, then run `./scripts/seed.py` (see the README). This prompt is for building your own variant from scratch, for example with a different curriculum.

Paste everything below the line into Claude Code, run from an empty clone of a new GitHub repo. Replace `punitpi/system-design-daily` with your own `owner/repo` first.

---

You're setting up my system design practice repo. Work through this end to end, then give me a short summary.

## Repo
- Remote: git@github.com:punitpi/system-design-daily.git
- Clone it (or use it if already cloned). Default branch: main.
- Use the GitHub CLI (`gh`) for labels, milestones, issues, and repo settings. First run `gh auth status`; if not authenticated, stop and tell me.
- Be idempotent: before creating any label, milestone, or issue, check whether it already exists and skip it if so. When listing, always pass an explicit large limit (e.g. `gh issue list --state all --limit 500`), because the default of 30 silently breaks the existence check.
- The backlog is **data in the repo**, not hand-made GitHub state (see sections 4–6), so anyone can recreate it with one command.

## 1. Repo structure
Create:

```
README.md
docs/how-to.md
templates/
  design.md
  concept.md
  teardown.md
concepts/.gitkeep
designs/.gitkeep
teardowns/.gitkeep
scripts/new.sh
scripts/seed.py
backlog/{issues,labels,milestones}.json
.github/workflows/seed.yml
docs/bootstrap-prompt.md
CLAUDE.md
.claude/skills/{today,tutor,quiz,polish}/SKILL.md
.claude/agents/design-reviewer.md
.github/ISSUE_TEMPLATE/teardown.md
```

### README.md
- One-paragraph purpose: daily system design practice, 30–45 min a day.
- A TL;DR line: `/today` → read the issue's resources → `/tutor` → write the entry from memory → `/polish` → explain it out loud in 2 minutes → commit with `Closes #N`. Link to `docs/how-to.md`.
- The weekly rhythm: 2 concept days, 3 design days, 1 teardown day (real engineering blog post), 1 review/rest day. Note that weeks 1–3 run concepts on all five weekday slots, because the design issues (#18+) depend on the fundamentals.
- How to work: pick the lowest-numbered open issue → `./scripts/new.sh <type> <slug> <issue#>` → fill in the template → commit with `Closes #<issue#>`.
- A "Use this for your own practice" section: click Use this template (the new repo must have no issues or PRs yet), run `./scripts/seed.py` (or the "Seed backlog" workflow), then `/today`. Mention that `"verified": false` resources were named from memory.
- A "Working with Claude" table listing `/today`, `/tutor`, `/quiz`, `/polish`, and the `design-reviewer` agent.
- A "Progress log" table (Date | Type | Topic | Issue | Link) that starts empty. It must be the **last thing in the file**, because `new.sh` appends to it.

### docs/how-to.md
- TL;DR at the top: the 7-step daily loop plus the phased weekly rhythm in one line.
- A daily loop table (step, time, what you do, tool).
- A day 1 walkthrough for issue #01, step by step, including an example `/tutor` exchange and the exact commit commands.
- The phased rhythm: weeks 1–3 concepts on weekdays; week 4 onward 2 concept / 3 design; every week one teardown day (`/today teardown`) and one `/quiz` review day.

### templates/design.md
Sections:
1. Requirements (functional / non-functional)
2. Back-of-the-envelope estimates (QPS, storage, bandwidth)
3. API
4. Data model
5. High-level design (Mermaid diagram placeholder in a ```mermaid block, plus a note that an Excalidraw PNG can go alongside)
6. Deep dive (1–2 components)
7. Bottlenecks & trade-offs
8. What I'd do differently / what I learned

Include a header line with placeholders `{{TITLE}}`, `{{DATE}}`, `{{ISSUE}}`.

### templates/concept.md
Same header line. Sections: What it is (in my own words) · Why it exists / problem it solves · How it works (diagram optional) · Trade-offs & when NOT to use it · Real-world example · Questions I still have.

### templates/teardown.md
Same header line. Sections: Source (link) · Company & problem · What they chose · Why (constraints that drove it) · Alternatives they rejected · What I'd steal for my own work.

### scripts/new.sh
- Usage: `./scripts/new.sh <concept|design|teardown> <slug> [issue-number]`
- Validate the arguments: the type must be one of the three, the slug must match `^[a-z0-9]+(-[a-z0-9]+)*$`, and the issue must be numeric. Otherwise print usage and exit non-zero.
- Resolve the repo root from the script's location, so it works from any directory.
- Uses today's date (YYYY-MM-DD).
- `concept` → creates `concepts/<date>-<slug>.md` from the template.
- `teardown` → creates `teardowns/<date>-<slug>.md` from the template.
- `design` → creates the folder `designs/<date>-<slug>/` with a `README.md` from the template.
- Replaces the title/date/issue placeholders. The title should be the slug turned into Title Case. A missing issue becomes `—`.
- Refuses to overwrite an existing file.
- Appends a row to the README progress table.
- Prints the created path.
- Make it executable, use `set -euo pipefail`, and keep it portable across macOS and Linux. Don't use `sed -i`; write `sed ... template > target` instead.
- Test it in a scratch copy: every type, with and without an issue number, overwrite refusal, bad arguments, and running from another directory.

## 2. Claude setup (for learning, not for doing the work)
Authorship rule: **I write the substance.** Claude may scaffold (create entries, suggest structure), polish (spelling, grammar, reorganizing my text into the template sections, fixing markdown/mermaid), and coach (questions, hints, pointing out gaps). It must not add technical claims that aren't in my text. Gaps get phrased as questions. If I explicitly insist on help with content, the added text gets marked `<!-- claude -->`.

Interactive roles must be **skills**, not subagents, because subagents run in the background and return one report, so they can't hold a conversation. Only the one-shot critique is an agent.

- **CLAUDE.md:** purpose, the authorship rule, the layout and conventions (the curriculum's source of truth is `backlog/*.json`, so edit that and run `seed.py` instead of creating the planned issues by hand; always create entries with `new.sh`, the progress log stays last, issue labels and milestones, commits use `<type>: <topic>` plus `Closes #N`, don't commit unless asked), a list of the tools, and a "tell me plainly when I'm wrong" line.
- **`/today [concept|design|teardown|review]`:** list open issues (`--limit 500`), take the lowest one (filtered by the type label if given), and infer the type from its label. Propose a slug: drop the `NN · ` prefix and any parenthetical, lowercase, collapse runs of non-alphanumerics to `-`, and trim. Confirm the exact `new.sh` command with me before running it, then show the issue's Goal / Cover / Done when and offer `/tutor`. For a teardown with no open issue, offer to create one once I name a post. For a review issue, open the existing entry. Never commit, never write content.
- **`/tutor [topic|issue#]`:** a Socratic session. Ask one question per message, using the issue's Cover list as the syllabus. Probe what I already know first, prefer "what breaks if…" questions, and escalate hints only when I'm stuck. Correct wrong answers by exposing the contradiction, then say it plainly. Finish with "what you now know" (in my words) and "still shaky". Never write the entry.
- **`/quiz`:** a recall drill on past entries. Prefer entries never quizzed, then the lowest score, then the oldest, and skip today's. Ask 3–5 questions one at a time, grade each right / partial / wrong against the entry, and log to `reviews/quiz-log.md` (Date | Entry | Score | Weak spots). If the score is under 60% or a weak spot repeats, propose a `review` issue and confirm before creating it.
- **`/polish <file>`:** spelling, grammar, restructuring into the template sections, and markdown/mermaid fixes only. Show the diff, then list gaps as questions. Never add or "improve" technical content.
- **`design-reviewer` agent** (tools: Read, Grep, Glob): interviewer-style critique of an entry, section by section. Give a verdict, then up to about 10 findings ranked by importance, each marked error / gap / nit and phrased as a question, then 3 follow-up questions and up to 2 genuine strengths. Point back to earlier entries where relevant. Never rewrite.

Skills go in `.claude/skills/<name>/SKILL.md` and agents in `.claude/agents/<name>.md`, each with `name` and `description` frontmatter (plus `tools` for the agent).

### .github/ISSUE_TEMPLATE/teardown.md
Frontmatter: `name: Teardown`, `title: "Teardown · "`, `labels: teardown`. Body: Source, Company & problem, and Done when (entry committed with `new.sh teardown`; can explain the key decision and its trade-off in 2 minutes).

## 3. Repo settings
- Description: "Daily system design practice: concepts, classic designs, and engineering-blog teardowns, 30–45 min a day."
- Topics: system-design, distributed-systems, software-architecture, scalability, interview-prep, learning-in-public, daily-practice. Check `gh repo edit --help` for the `--add-topic` syntax first.

## 4. Labels
Write them to `backlog/labels.json` as `{"labels": [{"name", "color", "description"}]}`, with:
- `concept` (blue)
- `design` (green)
- `teardown` (purple)
- `phase-1-fundamentals`
- `phase-2-patterns`
- `phase-3-designs`
- `review` (for later "v2" revisits)

## 5. Milestones
Write them to `backlog/milestones.json` as `{"milestones": [{"title"}]}`, with:
- "Phase 1 — Fundamentals"
- "Phase 2 — Patterns"
- "Phase 3 — Classic designs"

## 6. Issues, as data, plus the seeder
Write the 30 issues below **in this exact order** to `backlog/issues.json`. The issue number is the position in the list (1-based), and the GitHub title is `NN · <title>`. Format: `{"issues": [{"title", "labels": [type, phase-label], "milestone", "goal", "cover": [...], "resources": [{"text", "verified"}]}]}`. Use JSON rather than YAML so the seeder needs only Python's standard library. Set `"verified": false` on any resource you named without checking it against a source.

Then write `scripts/seed.py` (python3 standard library + `gh`, executable) and a manual `.github/workflows/seed.yml` (`workflow_dispatch`, `permissions: contents: read, issues: write`, `GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}`, runs `python3 scripts/seed.py --repo "$GITHUB_REPOSITORY"`). The seeder:
- takes `--repo` and `--dry-run`, and checks `gh auth status` first;
- **preflight, before changing anything:** if the first missing issue's number doesn't equal the repo's highest issue-or-PR number plus one (PRs share the sequence, so use the `issues` API endpoint, which returns both), stop with a clear message to use a fresh repo;
- creates missing labels, milestones, then issues, skipping anything that exists by exact name/title (always with `--limit 500`);
- creates issues strictly one at a time, and aborts if a created issue's URL doesn't end in the expected number;
- prints created/skipped counts for each kind.

Test the seeder offline against a fake `gh` on `PATH` that simulates GitHub's numbering: a fresh repo, a rerun (0 created), a repo with an existing PR (must stop before creating labels), a number drift mid-run (must abort), a partially seeded repo (must resume), and `--dry-run` (must change nothing). Also run `--dry-run` against the real repo and compare each generated issue body to the live one.

Body template for each issue (rendered by the seeder):

```
## Goal
<one sentence>

## Cover
- [ ] <key point>
- [ ] ...

## Resources
<1–2 well-known resources>

## Done when
- [ ] Entry committed using the matching template
- [ ] Can explain it out loud in 2 minutes without notes
```

For design issues, add this checklist item to "Done when": `Diagram included (Mermaid or Excalidraw)`.

**Resources must be verified, not recalled.** Fetch the system-design-primer README and only use anchors that its own README links to. Check DDIA and Alex Xu (Vol. 1 and 2) chapter titles against a published table of contents. Cite DDIA as "(1st ed.)" without chapter numbers, because the 2nd edition renumbers them. Only link a URL after fetching it successfully; otherwise name the resource without a link. Never invent URLs.

### Phase 1 — Fundamentals (concept)
01. Back-of-the-envelope estimation — powers of 2, latency numbers, QPS/storage/bandwidth math, peak vs average
02. Load balancing — L4 vs L7, round robin / least connections / hashing, health checks, sticky sessions
03. Caching strategies — cache-aside, write-through, write-back, eviction (LRU/LFU), invalidation, stampede/thundering herd
04. Database replication — leader-follower, multi-leader, leaderless, replication lag, read-your-writes
05. Sharding & partitioning — range vs hash, hotspots, rebalancing, cross-shard queries
06. Consistent hashing — the hash ring, virtual nodes, minimal remapping
07. CAP, PACELC & consistency models — strong, eventual, causal, linearizability, quorum (R+W>N)
08. Message queues & pub/sub — queue vs log (RabbitMQ vs Kafka), consumer groups, at-most/at-least/exactly-once, ordering
09. Idempotency & retries — idempotency keys, dedup, safe retries, exactly-once as an illusion
10. Rate limiting — token bucket, leaky bucket, fixed/sliding window; then design a distributed rate limiter (Redis, race conditions)

### Phase 2 — Patterns (concept)
11. API design — REST vs gRPC vs GraphQL, pagination (offset vs cursor), versioning, error design
12. Event-driven architecture, CQRS & event sourcing — when they help, when they hurt
13. Distributed transactions — 2PC vs saga (choreography vs orchestration), transactional outbox
14. Resilience patterns — timeouts, retries with backoff + jitter, circuit breaker, bulkhead, load shedding, graceful degradation
15. Consensus & leader election — Raft basics, split brain, fencing tokens, where etcd/ZooKeeper fit
16. Probabilistic data structures — Bloom filter, HyperLogLog, count-min sketch, and where each shows up
17. Storage engines & indexing — B-tree vs LSM tree, write/read amplification, inverted index for search

### Phase 3 — Classic designs (design)
18. URL shortener — ID generation, base62, redirects (301 vs 302), read-heavy caching, analytics
19. Unique ID generator — UUID vs DB sequence vs Snowflake, clock skew, sortability
20. Distributed key-value store — Dynamo-style: partitioning, replication, quorum, vector clocks, hinted handoff, anti-entropy
21. Notification system — push/SMS/email fan-out, templates, user preferences, retries, dedup, rate limits
22. Chat system (WhatsApp-like) — WebSockets, presence, message ordering, delivery receipts, offline sync, group chat
23. News feed (Twitter/Instagram) — fan-out on write vs read, celebrity problem, ranking, feed cache
24. Web crawler — URL frontier, politeness, dedup (content hashing), robots.txt, distributed workers
25. Search autocomplete / typeahead — trie, top-k per prefix, offline aggregation, caching at the edge
26. Distributed job scheduler — cron at scale, leader election, exactly-once execution, retries, visibility timeouts
27. Video streaming platform (YouTube/Netflix) — upload pipeline, transcoding, adaptive bitrate (HLS/DASH), CDN
28. Proximity service / ride-sharing (Yelp/Uber) — geohash vs quadtree, location updates at scale, matching
29. Payment system — idempotency, double-entry ledger, reconciliation, PSP integration, exactly-once money movement
30. Observability platform (capstone) — metrics/logs/traces ingestion at scale, high cardinality, retention tiers, multi-tenant query (compare to how Loki/Mimir/Tempo solve it)

## 7. Make it a template (ask me first)
After I confirm, mark the repo as a template with `gh repo edit --template`. Don't do this unprompted.

## 8. Commit & push
- Commit the structure with a message like "chore: scaffold repo, templates, and new-entry script", and the Claude setup separately with "chore: add Claude learning setup". No AI attribution trailers.
- Push to main.

## 9. Verify, then report back
Verify:
- Issues #1–30 map to `01`–`30` in order, with the right labels and milestones.
- Rerunning `scripts/seed.py` creates 0 and skips everything.
- The workflow YAML is valid. Say plainly that I haven't run it on GitHub unless you have.
- The description and topics are set.
- `scripts/new.sh` is committed with mode `100755`.

Then give me:
- The list of files created
- Counts of labels, milestones, and issues created vs skipped
- Which resources were verified and which were only named
- The link to the issues page
- An example command to start issue #01
