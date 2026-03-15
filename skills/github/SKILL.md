---
name: github
description: "Use this skill for any GitHub operations via gh CLI. Triggers: github, gh, issue, pull request, PR, repository, workflow, actions, merge, branch, commit, fork, clone, milestone, label, assignee, reviewer, CI, CD, pipeline, release, gist, notifications, stars, watch, collaborator."
---

# GitHub CLI Skill

Interact with GitHub via `gh` CLI with safety guardrails.

## Prerequisites

Before using GitHub commands:

1. **Verify gh CLI installed:** `gh --version`
2. **Verify authentication:** `gh auth status`
3. If not authenticated: `gh auth login`

## Quick Reference

| Task | Command |
|------|---------|
| List my issues | `gh issue list --assignee @me` |
| List my PRs | `gh pr list --author @me` |
| Create issue | `gh issue create --title "..." --body "..."` |
| Create PR | `gh pr create --title "..." --body "..."` |
| View issue | `gh issue view 123` |
| View PR | `gh pr view 123` |
| Check CI status | `gh run list --limit 5` |
| Clone repo | `gh repo clone owner/repo` |

## Safety Rules (CRITICAL)

### NEVER Execute (Blocked)

These commands are blocked and must not be executed:

- `gh repo delete` - Irreversible repository deletion
- `gh api DELETE /repos/*` - API-level deletion
- `git push --force origin main` - Overwrites protected main branch
- `git push --force origin master` - Overwrites protected master branch
- Bulk close all issues without explicit confirmation

### Confirmation Required

These commands require explicit user confirmation before execution:

- `gh pr merge --admin` - Bypasses branch protection
- `gh pr close` - Closes PR without merging
- `gh workflow disable` - Disables CI workflow
- `gh release delete` - Removes release

When user requests a blocked command:
1. Explain why it's blocked
2. Suggest a safer alternative
3. Do NOT execute even if user insists

## Workflow Routing

### Simple Operations (Direct gh CLI)

For single-item operations, use gh commands directly:

```bash
# Issues
gh issue list --assignee @me
gh issue create --title "Bug: ..." --body "Description"
gh issue edit 123 --add-label bug

# PRs
gh pr create --title "Add feature" --body "Description"
gh pr view 123
gh pr merge 123 --squash

# Workflows
gh run list --limit 10
gh run view 123 --log-failed
```

### Bulk Operations (Python Scripts)

For bulk operations, use the provided Python scripts:

```bash
# Bulk label issues
python scripts/bulk_issues.py label --query "is:open no:label" --add triage

# Bulk assign issues
python scripts/bulk_issues.py assign --query "is:open label:bug" --assignee @me

# Bulk close issues
python scripts/bulk_issues.py close --numbers 1,2,3 --reason completed
```

### Safety Validation

Before executing any command, validate with safety_check.py:

```bash
python scripts/safety_check.py "gh repo delete owner/repo"
# Output: BLOCKED: gh repo delete — Irreversible repository deletion
```

### PR Lifecycle

For full PR workflows:

```bash
python scripts/pr_workflow.py create --branch feat/x --title "Add X"
python scripts/pr_workflow.py review --pr 123 --approve
python scripts/pr_workflow.py merge --pr 123 --squash
python scripts/pr_workflow.py status --pr 123
```

### CI Monitoring

For GitHub Actions monitoring:

```bash
python scripts/workflow_status.py list --workflow build.yml --limit 5
python scripts/workflow_status.py wait --run-id 123 --timeout 600
python scripts/workflow_status.py rerun --run-id 123 --failed-only
python scripts/workflow_status.py logs --run-id 123
```

## Error Handling

| Error | Recovery |
|-------|----------|
| `gh: command not found` | Install gh CLI: https://cli.github.com |
| `not logged in` | Run `gh auth login` |
| `repository not found` | Specify `--repo owner/name` or cd to repo |
| `permission denied` | Check repo access permissions |

## References

For detailed command documentation:

- `references/issues.md` - Issue management workflows
- `references/prs.md` - Pull request operations
- `references/repos.md` - Repository operations
- `references/actions.md` - GitHub Actions/CI
- `references/safety.md` - Complete blocked command list
