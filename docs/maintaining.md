# Maintaining this repo (for the repo owner)

This page matters only if you are the maintainer of the original repo. If you forked it for your own practice, you can ignore it.

## Branches

- `main`: the maintainer's personal practice log. Entries, progress-log rows and `reviews/quiz-log.md` live here. It is the default branch, so `Closes #N` in a commit closes the issue.
- `template`: a clean copy that people start from after forking. It must never contain entries, progress-log rows or quiz logs.

## Rules

1. Change tooling, templates, skills, the backlog JSON, and docs on `template` first.
2. Then bring them into `main`: `git switch main && git merge template`.
3. Never merge `main` into `template`, and never create entries while `template` is checked out. `new.sh` writes into the working tree and appends to `README.md`.
4. The README's progress-log table sits at the bottom of the file so merges from `template` rarely conflict.
