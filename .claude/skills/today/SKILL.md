---
name: today
description: Start today's system design practice entry. Picks the lowest-numbered open GitHub issue (optionally filtered by type: concept, design, teardown, review), creates the entry with scripts/new.sh, and shows the issue's checklist. Use when the user says /today, "what's next", or "start today's entry".
---

# Start today's entry

Optional argument: `concept`, `design`, `teardown`, or `review`. If none is given, take the lowest open issue of any type.

1. **Find the issue.**
   ```sh
   gh issue list --state open --limit 500 --json number,title,labels,body
   ```
   Filter by the type label if an argument was given, then take the lowest `number`. If nothing matches, say so. For `teardown`, offer to open a new issue from the teardown template (`gh issue create --label teardown`) once the user names a blog post. Don't invent one.

2. **Work out the type** from the labels (`concept`, `design`, `teardown`). A `review` issue revisits an existing entry, so find that entry and open it rather than creating a new one, then suggest `/quiz` or `/tutor` on it.

3. **Propose a slug** from the title. Drop the `NN · ` prefix and any parenthetical, lowercase it, replace each run of non-alphanumeric characters with a single `-`, and trim leading and trailing hyphens. For example, `01 · Back-of-the-envelope estimation` becomes `back-of-the-envelope-estimation`, `07 · CAP, PACELC & consistency models` becomes `cap-pacelc-consistency-models`, and `22 · Chat system (WhatsApp-like)` becomes `chat-system`. Show the exact command and confirm with the user before running it:
   ```sh
   ./scripts/new.sh <type> <slug> <issue#>
   ```
   If new.sh refuses because the file exists, report it and stop. Don't delete or overwrite anything.

4. **Show the plan for today.** Print the created path, then the issue's **Goal**, **Cover** checklist, and **Done when** checklist.

5. **Offer the next step**, e.g. "Want a `/tutor` session on this first, or are you writing straight away?"

Never commit and never write the entry content. The user does both.
