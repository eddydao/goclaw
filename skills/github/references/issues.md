# Issue Management

Complete guide to GitHub issue operations via `gh` CLI.

## Listing Issues

```bash
# All open issues in current repo
gh issue list

# Assigned to me
gh issue list --assignee @me

# By label
gh issue list --label bug
gh issue list --label "priority:high"

# By milestone
gh issue list --milestone "v1.0"

# By state
gh issue list --state open
gh issue list --state closed
gh issue list --state all

# Limit results
gh issue list --limit 50

# JSON output for parsing
gh issue list --json number,title,state,labels,assignees
```

## Creating Issues

```bash
# Basic issue
gh issue create --title "Bug: Login fails" --body "Steps to reproduce..."

# With labels
gh issue create --title "Bug" --label bug,urgent

# With assignee
gh issue create --title "Task" --assignee @me

# With milestone
gh issue create --title "Feature" --milestone "v1.0"

# Using template
gh issue create --template bug_report.md

# Open editor for body
gh issue create --title "Feature request"
```

## Viewing Issues

```bash
# View issue details
gh issue view 123

# View in browser
gh issue view 123 --web

# JSON output
gh issue view 123 --json number,title,body,comments
```

## Editing Issues

```bash
# Add label
gh issue edit 123 --add-label bug

# Remove label
gh issue edit 123 --remove-label wontfix

# Add assignee
gh issue edit 123 --add-assignee user1

# Change title
gh issue edit 123 --title "New title"

# Add to milestone
gh issue edit 123 --milestone "v1.0"
```

## Closing Issues

```bash
# Close issue
gh issue close 123

# Close with reason
gh issue close 123 --reason completed
gh issue close 123 --reason "not_planned"
gh issue close 123 --reason duplicate

# Reopen issue
gh issue reopen 123
```

## Search Syntax

Use `--search` for advanced queries:

```bash
# By author
gh issue list --search "author:username"

# By creation date
gh issue list --search "created:>2024-01-01"
gh issue list --search "updated:<2024-06-01"

# No label
gh issue list --search "no:label"

# No assignee
gh issue list --search "no:assignee"

# Combined
gh issue list --search "is:open label:bug no:assignee"
```

## Common Triage Workflow

```bash
# 1. Find unlabeled issues
gh issue list --search "no:label" --limit 20

# 2. Bulk add triage label
python scripts/bulk_issues.py label --query "no:label" --add triage

# 3. Review and categorize
gh issue view 123
gh issue edit 123 --add-label bug --add-assignee @me

# 4. Check your assignments
gh issue list --assignee @me --state open
```

## Issue Templates

```bash
# List available templates
ls .github/ISSUE_TEMPLATE/

# Create with specific template
gh issue create --template bug_report.md
gh issue create --template feature_request.md
```

## Comments

```bash
# Add comment
gh issue comment 123 --body "Working on this"

# View comments (in JSON)
gh issue view 123 --json comments
```
