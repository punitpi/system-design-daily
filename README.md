# system-design-daily

Daily system design practice, 30–45 minutes a day. The goal is to build real intuition for distributed systems by learning the fundamentals, working through classic designs, and reading how real companies solved real problems. Every entry is written in my own words. If I can't explain a topic out loud in two minutes, I haven't finished learning it.

## TL;DR

`/today` → read the issue's resources → `/tutor` → write the entry from memory → `/polish` → explain it out loud in 2 minutes → commit with `Closes #N`.

The full guide, with a day 1 walkthrough, is in [docs/how-to.md](docs/how-to.md). To recreate this repo from scratch, use [docs/bootstrap-prompt.md](docs/bootstrap-prompt.md).

## Use this for your own practice

The curriculum is data, not hand-made GitHub state: `backlog/issues.json` (30 issues, in learning order), `backlog/labels.json` and `backlog/milestones.json`. `scripts/seed.py` turns them into real labels, milestones and issues, and is safe to rerun.

1. Click **Use this template** to create your own repo. It should be brand new, with no issues or pull requests yet, so issue numbers line up with the learning order. The seeder stops before changing anything if they don't.
2. Seed the backlog, either way:
   - Locally, with the [GitHub CLI](https://cli.github.com/) signed in: `./scripts/seed.py` (add `--dry-run` to preview)
   - On GitHub: **Actions** tab, **Seed backlog**, **Run workflow**
3. Open Claude Code in the repo and run `/today`.

Use the template button rather than forking. If you do fork, first enable Issues (Settings, then Features) and enable workflows in the Actions tab.

Edit the JSON before seeding to make the curriculum your own. Resources marked `"verified": false` were named from memory, so check them before relying on them.

## Weekly rhythm

| Days | Type | What |
| --- | --- | --- |
| 2 | Concept | One building block (caching, replication, consensus, ...) using `templates/concept.md` |
| 3 | Design | One end-to-end system using `templates/design.md` |
| 1 | Teardown | One real engineering blog post using `templates/teardown.md` |
| 1 | Review / rest | Revisit weak spots (`review` label) or take the day off |

Weeks 1–3 run concepts on all five weekday slots, because the design issues (#18+) depend on the fundamentals. See [docs/how-to.md](docs/how-to.md#the-weekly-rhythm-in-phases).

## How to work

1. Pick the **lowest-numbered open issue** in [Issues](https://github.com/punitpi/system-design-daily/issues). Issue numbers follow the learning sequence.
2. Create the entry:
   ```sh
   ./scripts/new.sh <concept|design|teardown> <slug> <issue#>
   # e.g. ./scripts/new.sh concept back-of-the-envelope-estimation 1
   ```
   This creates the file from the matching template and adds a row to the progress log below.
3. Fill in the template.
4. Commit with `Closes #<issue#>` in the message.

## Layout

```
concepts/    YYYY-MM-DD-<slug>.md
designs/     YYYY-MM-DD-<slug>/README.md  (plus diagrams)
teardowns/   YYYY-MM-DD-<slug>.md
templates/   entry templates
scripts/     new.sh (create an entry), seed.py (create the backlog)
backlog/     issues.json, labels.json, milestones.json (the curriculum)
docs/        how-to.md, bootstrap-prompt.md
```

## Working with Claude

The repo includes a Claude Code setup (`CLAUDE.md`, `.claude/`). Claude coaches and polishes, but I do the writing.

| Command | What it does |
| --- | --- |
| `/today [type]` | Picks the next open issue, creates the entry, and shows the checklist |
| `/tutor [topic]` | Socratic session: Claude asks the questions and I work out the answers |
| `/quiz` | Recall drill on past entries, logged to `reviews/quiz-log.md` |
| `/polish <file>` | Fixes spelling, structure, and markdown/mermaid. Doesn't add content |
| `design-reviewer` agent | Critiques an entry the way an interviewer would |

## Progress log

| Date | Type | Topic | Issue | Link |
| --- | --- | --- | --- | --- |
