# system-design-daily

Daily system design practice, 30–45 minutes a day. The goal is to build real intuition for distributed systems by learning the fundamentals, working through classic designs, and reading how real companies solved real problems. Every entry is written in my own words. If I can't explain a topic out loud in two minutes, I haven't finished learning it.

## Weekly rhythm

| Days | Type | What |
| --- | --- | --- |
| 2 | Concept | One building block (caching, replication, consensus, ...) using `templates/concept.md` |
| 3 | Design | One end-to-end system using `templates/design.md` |
| 1 | Teardown | One real engineering blog post using `templates/teardown.md` |
| 1 | Review / rest | Revisit weak spots (`review` label) or take the day off |

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
scripts/     new.sh
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
