# system-design-daily

Daily system design practice, 30–45 minutes a day. The goal is to build real intuition for distributed systems by learning the fundamentals, working through classic designs, and reading how real companies solved real problems. Every entry is written in my own words. If I can't explain a topic out loud in two minutes, I haven't finished learning it.

## TL;DR

`/today` → read the issue's resources → `/tutor` → write the entry from memory → `/polish` → explain it out loud in 2 minutes → commit with `Closes #N`.

To get your own copy, see [Get your own copy](#get-your-own-copy-fork). The full daily guide, with a day 1 walkthrough, is in [docs/how-to.md](docs/how-to.md). To build a variant from scratch, use [docs/bootstrap-prompt.md](docs/bootstrap-prompt.md).

## Get your own copy (fork)

This repo is my own practice log, so `main` has my entries. A clean copy with no entries lives on the **`template`** branch. Fork the repo and start from that branch.

You need a GitHub account and [Claude Code](https://claude.com/claude-code). Everything up to step 3 happens in the browser.

1. **Fork** this repo. Untick **Copy the DEFAULT branch only** so you also get the `template` branch.
2. **In your fork's settings:**
   - **Settings, then General, then Features:** turn **Issues** on (forks have it off by default).
   - **Settings, then Branches:** change the default branch to `template`, so `Closes #N` in your commits closes issues.
   - **Actions tab:** enable workflows.
3. **Seed the backlog:** in the **Actions** tab, pick **Seed backlog** and click **Run workflow**. It creates 7 labels, 3 milestones and issues #1-#30 in learning order. It uses GitHub's built-in token, so you don't create any secret, and it is safe to run again.
4. **Start day 1:** clone your fork, switch to the clean branch, and open Claude Code.
   ```sh
   gh repo clone <you>/system-design-daily && cd system-design-daily
   git switch template
   claude        # then type: /today
   ```

Your fork's `main` branch will have my entries. Ignore it or delete it (`git push origin --delete main`).

### Prefer the terminal to the workflow?

You need the [GitHub CLI](https://cli.github.com/) signed in (`gh auth login`) and Python 3. Replace step 3 with:

```sh
ME=$(gh api user --jq .login)
./scripts/seed.py --repo "$ME/system-design-daily"     # add --dry-run to preview first
```

Always pass `--repo` in a fork. After `gh repo fork --clone`, plain `gh` commands default to *my* repo, not yours. You can also do steps 1 and 2 from the terminal: `gh repo fork punitpi/system-design-daily --clone`, then `gh repo edit "$ME/system-design-daily" --default-branch template --enable-issues`.

### Good to know

- **Start with a fork that has no issues or pull requests.** Issue numbers must line up with the learning order. The seeder checks this and stops before changing anything.
- **Trade-offs of a fork:** commits on a fork don't count toward your GitHub contribution graph. In return, you can pull my later fixes with **Sync fork** (or `gh repo sync`) on the `template` branch. Expect some merge conflicts in `README.md` once you start logging progress.
- **Make it your own.** The curriculum is data: `backlog/issues.json`, `backlog/labels.json` and `backlog/milestones.json`. Edit them before seeding. Resources marked `"verified": false` were named from memory, so check them before relying on them.

**Tested:** the Seed backlog workflow on an empty repo (it created 7 labels, 3 milestones and 30 issues matching this repo, and a second run created nothing), and `seed.py` against a simulated `gh` (fresh repo, rerun, existing PR, number drift, partial run, dry run, Issues disabled). **Not yet tested:** the fork steps end to end (forking with all branches, changing the default branch, enabling workflows in a fork).

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
docs/        how-to.md, bootstrap-prompt.md, maintaining.md
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
