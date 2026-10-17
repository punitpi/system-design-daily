#!/usr/bin/env python3
"""Create the labels, milestones and issues described in backlog/*.json.

Idempotent: anything that already exists (by exact name/title) is skipped, so it is safe to rerun.
Needs only python3 and an authenticated GitHub CLI (`gh auth status`).

Usage: scripts/seed.py [--repo OWNER/REPO] [--dry-run]
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

BACKLOG = Path(__file__).resolve().parent.parent / "backlog"


def gh(*args, check=True):
    out = subprocess.run(["gh", *args], capture_output=True, text=True)
    if check and out.returncode != 0:
        sys.exit(f"gh {' '.join(args[:3])} failed: {out.stderr.strip()}")
    return out


def load(name):
    return json.loads((BACKLOG / name).read_text(encoding="utf-8"))


def issue_body(issue):
    done = ["Entry committed using the matching template", "Can explain it out loud in 2 minutes without notes"]
    if "design" in issue["labels"]:
        done.append("Diagram included (Mermaid or Excalidraw)")
    lines = ["## Goal", issue["goal"], "", "## Cover"]
    lines += [f"- [ ] {c}" for c in issue["cover"]]
    lines += ["", "## Resources"] + [f"- {r['text']}" for r in issue["resources"]]
    lines += ["", "## Done when"] + [f"- [ ] {d}" for d in done]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--repo", help="OWNER/REPO (default: the repo of the current directory)")
    ap.add_argument("--dry-run", action="store_true", help="show what would be created, change nothing")
    args = ap.parse_args()

    if gh("auth", "status", check=False).returncode != 0:
        sys.exit("Not authenticated: run `gh auth login` (or set GH_TOKEN) and retry.")
    repo = args.repo or gh("repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner").stdout.strip()
    dry = args.dry_run
    print(f"Repo: {repo}{' (dry run)' if dry else ''}")

    # Forks (and some repos) have Issues switched off, which would fail confusingly later.
    if gh("repo", "view", repo, "--json", "hasIssuesEnabled", "--jq", ".hasIssuesEnabled").stdout.strip() != "true":
        sys.exit(f"Issues are disabled on {repo}. Enable them under Settings > General > Features > Issues, then rerun.")

    # Preflight, before changing anything: issue numbers follow the learning order, so the repo's
    # issue/PR counter must line up with the first issue still to be created.
    issues = load("issues.json")["issues"]
    titles = [f"{i:02d} · {iss['title']}" for i, iss in enumerate(issues, 1)]
    have_issues = set(gh("issue", "list", "-R", repo, "--state", "all", "--limit", "500", "--json", "title", "--jq", ".[].title").stdout.split("\n"))
    # The issues endpoint returns PRs too, which share the number sequence.
    top = int(gh("api", f"repos/{repo}/issues?state=all&per_page=1&sort=created&direction=desc", "--jq", ".[0].number // 0").stdout.strip() or 0)
    first_missing = next((n for n, t in enumerate(titles, 1) if t not in have_issues), None)
    if first_missing is not None and top != first_missing - 1:
        sys.exit(f"Stopping before changing anything: the next GitHub number would be {top + 1}, but "
                 f"'{titles[first_missing - 1]}' must be #{first_missing}. Issues/PRs already exist in {repo}, so numbers "
                 f"would not match the learning order. Use a fresh repo (or delete the extra issues) and rerun.")

    # Labels
    have = set(gh("label", "list", "-R", repo, "--limit", "500", "--json", "name", "--jq", ".[].name").stdout.split("\n"))
    made = skipped = 0
    for lab in load("labels.json")["labels"]:
        if lab["name"] in have:
            skipped += 1
            continue
        if not dry:
            gh("label", "create", lab["name"], "-R", repo, "--color", lab["color"], "--description", lab["description"])
        print(f"label     + {lab['name']}")
        made += 1
    print(f"labels:     created={made} skipped={skipped}")

    # Milestones
    have = set(gh("api", f"repos/{repo}/milestones?state=all&per_page=100", "--jq", ".[].title").stdout.split("\n"))
    made = skipped = 0
    for ms in load("milestones.json")["milestones"]:
        if ms["title"] in have:
            skipped += 1
            continue
        if not dry:
            gh("api", f"repos/{repo}/milestones", "-f", f"title={ms['title']}")
        print(f"milestone + {ms['title']}")
        made += 1
    print(f"milestones: created={made} skipped={skipped}")

    # Issues: one at a time and in order; stop at the first mismatch rather than let numbers drift.
    made = skipped = 0
    for n, (title, iss) in enumerate(zip(titles, issues), 1):
        if title in have_issues:
            skipped += 1
            continue
        print(f"issue     + {title}")
        if not dry:
            cmd = ["issue", "create", "-R", repo, "--title", title, "--body", issue_body(iss), "--milestone", iss["milestone"]]
            for lab in iss["labels"]:
                cmd += ["--label", lab]
            url = gh(*cmd).stdout.strip()
            if not url.endswith(f"/{n}"):
                sys.exit(f"Created {url} but expected issue #{n}; stopping so numbering does not drift further.")
        made += 1
    print(f"issues:     created={made} skipped={skipped}")


if __name__ == "__main__":
    main()
