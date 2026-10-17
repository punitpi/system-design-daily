---
name: quiz
description: Recall drill on the user's past system design entries (spaced-repetition style). Asks questions from what the user wrote, grades the answers, and logs results to reviews/quiz-log.md. Use when the user says /quiz, "quiz me", "test me", or on a review day.
---

# Recall quiz

Optional argument: an entry path, a topic, or a count (default: 1 entry, 4 questions).

## 1. Pick the entry

- List entries: `concepts/*.md`, `designs/*/README.md`, `teardowns/*.md`.
- Read `reviews/quiz-log.md` if it exists.
- Prefer entries that have never been quizzed, then the ones with the lowest last score, then the ones quizzed longest ago. Don't pick anything written today.
- If there are no entries yet, say so and suggest `/today`.

## 2. Ask

- Ask 3–5 questions **one at a time**, drawn from what the entry actually says. Mix recall ("What are the three replication topologies?"), application ("Your feed cache hit rate drops to 40%. What do you check first?"), and trade-off questions ("When would you pick 302 over 301?").
- Don't show the entry or hint at the answer before they respond.

## 3. Grade

After each answer, compare it to the entry and say **right / partial / wrong** with a one-line reason. If the entry itself is wrong or thin on the point, say so, because that's a fix for the entry, not a failed answer.

## 4. Log and follow up

Append to `reviews/quiz-log.md` (create it with this header if missing):

```markdown
# Quiz log

| Date | Entry | Score | Weak spots |
| --- | --- | --- | --- |
```

Row: `| YYYY-MM-DD | <path> | <right>/<total> | <short phrases> |`

If the score is under 60% or a weak spot repeats from a previous quiz, suggest a revisit issue. Show the command and confirm before running it:

```sh
gh issue create --title "Review · <topic>" --label review --body "Revisit <path>. Weak spots: ..."
```

Don't commit. The user does that.
