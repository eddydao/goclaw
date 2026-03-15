# Pull Request Management

Complete guide to GitHub PR operations via `gh` CLI.

## Creating PRs

```bash
# Basic PR (prompts for details)
gh pr create

# With title and body
gh pr create --title "Add feature X" --body "Description..."

# Draft PR
gh pr create --draft --title "WIP: Feature"

# Target specific base branch
gh pr create --base develop

# Request reviewers
gh pr create --reviewer user1,user2

# Add assignee
gh pr create --assignee @me

# Add labels
gh pr create --label enhancement,needs-review

# Fill from commit messages
gh pr create --fill
```

## Listing PRs

```bash
# Open PRs
gh pr list

# Your PRs
gh pr list --author @me

# PRs to review
gh pr list --search "review-requested:@me"

# By state
gh pr list --state open
gh pr list --state closed
gh pr list --state merged
gh pr list --state all

# By base branch
gh pr list --base main

# JSON output
gh pr list --json number,title,state,author,headRefName
```

## Viewing PRs

```bash
# View PR details
gh pr view 123

# View in browser
gh pr view 123 --web

# View diff
gh pr diff 123

# JSON with all fields
gh pr view 123 --json title,body,reviews,statusCheckRollup
```

## Reviewing PRs

```bash
# Approve
gh pr review 123 --approve

# Approve with comment
gh pr review 123 --approve --body "LGTM!"

# Request changes
gh pr review 123 --request-changes --body "Please fix..."

# Comment only (no approval)
gh pr review 123 --comment --body "Question about line 42..."
```

## Merging PRs

```bash
# Default merge
gh pr merge 123

# Squash merge
gh pr merge 123 --squash

# Rebase merge
gh pr merge 123 --rebase

# Merge commit
gh pr merge 123 --merge

# Auto-merge when checks pass
gh pr merge 123 --auto --squash

# Delete branch after merge
gh pr merge 123 --delete-branch
```

## Updating PRs

```bash
# Edit title/body
gh pr edit 123 --title "New title"
gh pr edit 123 --body "Updated description"

# Add reviewers
gh pr edit 123 --add-reviewer user1

# Add labels
gh pr edit 123 --add-label needs-review

# Mark as ready (from draft)
gh pr ready 123
```

## Closing PRs

```bash
# Close without merge
gh pr close 123

# Reopen
gh pr reopen 123
```

## Checking Out PRs

```bash
# Checkout PR branch locally
gh pr checkout 123

# Checkout and create local branch
gh pr checkout 123 --branch my-local-branch
```

## PR Checks

```bash
# View check status
gh pr checks 123

# Wait for checks to complete
gh pr checks 123 --watch

# View failed checks
gh pr checks 123 --fail
```

## Comments

```bash
# Add comment
gh pr comment 123 --body "Thanks for the review!"

# Reply to review thread (use API)
gh api repos/{owner}/{repo}/pulls/123/comments
```

## Common Workflows

### Create and Review Flow
```bash
# 1. Create PR
gh pr create --title "Add feature" --body "Description" --reviewer teammate

# 2. Check status
gh pr view 123

# 3. After approval, merge
gh pr merge 123 --squash --delete-branch
```

### Code Review Flow
```bash
# 1. List PRs needing review
gh pr list --search "review-requested:@me"

# 2. Checkout and review
gh pr checkout 123
# ... review code ...

# 3. Approve
gh pr review 123 --approve --body "Looks good!"
```
