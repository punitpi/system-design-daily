---
name: polish
description: Polish a system design entry the user wrote. Fixes spelling, grammar, structure (moves content into the right template sections) and markdown/mermaid syntax without adding technical content. Lists gaps as questions. Use when the user says /polish, "clean this up", "spell check", or "make this proper".
---

# Polish an entry

Argument: path to an entry. With no argument, use the most recent row in the README progress log.

## Allowed

- Spelling, grammar, punctuation, consistent terminology (e.g. "leader/follower" throughout, not mixed with "master/slave").
- Restructuring: move existing text under the right template heading (see `templates/<type>.md`) and restore any template headings that were deleted.
- Turning run-on notes into bullets or tables, as long as the meaning is the same.
- Fixing markdown and Mermaid syntax so it renders. Keep the diagram's nodes and edges the same.
- Fixing obvious unit typos only where the user's own working makes the intent unambiguous (e.g. "10 GB/s" when their arithmetic shows 10 MB/s). Call out every one of these.

## Not allowed

- Adding facts, numbers, components, trade-offs, or examples that aren't in the text.
- "Improving" a technical claim. If a claim looks wrong, list it as a question instead.
- Removing content, unless it's an exact duplicate.

## Process

1. Read the entry and its template.
2. Make the edits, then show a concise summary of the change types and the `git diff` for the file. If the file isn't tracked yet, show the before/after instead.
3. After the diff, list **Gaps & questions**: empty sections, claims that look wrong, and missing failure modes, each phrased as a question for the user to answer. Suggest the `design-reviewer` agent for a deeper critique.

Don't commit.
