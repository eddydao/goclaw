# Safety Rules

Critical safety rules for GitHub CLI operations.

## BLOCKED Commands (NEVER Execute)

These commands are blocked and must NOT be executed under any circumstances:

| Command | Reason | Alternative |
|---------|--------|-------------|
| `gh repo delete` | Irreversible repository deletion | Archive instead: `gh repo archive` |
| `gh api DELETE /repos/*` | API-level repo deletion | Same as above |
| `git push --force origin main` | Overwrites main branch history | Use `--force-with-lease` |
| `git push --force origin master` | Overwrites master branch history | Use `--force-with-lease` |
| `git push -f origin main` | Short form of force push | Use `--force-with-lease` |
| Bulk close all issues | Mass data loss | Close individually with review |

### Why These Are Blocked

**Repository Deletion:**
- Cannot be undone
- Loses all issues, PRs, wikis, actions history
- May affect dependent projects
- Alternative: Archive preserves data but prevents changes

**Force Push to Main:**
- Rewrites shared history
- Breaks other developers' work
- May lose commits
- Alternative: `--force-with-lease` checks for upstream changes first

## CONFIRMATION Required

These commands require explicit user confirmation:

| Command | Risk | Confirmation Phrase |
|---------|------|---------------------|
| `gh pr merge --admin` | Bypasses branch protection | "I confirm admin merge" |
| `gh pr close` | Closes PR without merging | "I confirm close without merge" |
| `gh workflow disable` | Stops CI for repository | "I confirm disable CI" |
| `gh release delete` | Removes published release | "I confirm delete release" |
| `gh repo archive` | Makes repo read-only | "I confirm archive" |

### Confirmation Flow

When user requests a confirmation-required command:

1. **Explain the risk** clearly
2. **Ask for confirmation** using the exact phrase
3. **Execute only after** receiving exact confirmation
4. **Log the action** for audit trail

Example:
```
User: "Close PR #123"
Agent: "This will close PR #123 without merging the code.
        To proceed, confirm with: 'I confirm close without merge'"
User: "I confirm close without merge"
Agent: [executes gh pr close 123]
```

## Safe Alternatives

### Instead of Force Push
```bash
# BLOCKED
git push --force origin main

# SAFE: Force with lease (checks for upstream changes)
git push --force-with-lease origin main

# SAFER: Create new commit to fix
git revert <commit>
git push origin main
```

### Instead of Repo Delete
```bash
# BLOCKED
gh repo delete owner/repo

# SAFE: Archive (reversible)
gh repo archive owner/repo

# SAFE: Make private
gh repo edit --visibility private
```

### Instead of Bulk Close
```bash
# BLOCKED
gh issue close --all

# SAFE: Review and close individually
gh issue list --state open
gh issue close 123 --reason completed
```

## Validation Script

Use `safety_check.py` to validate commands:

```bash
# Check if command is allowed
python scripts/safety_check.py "gh repo delete owner/repo"
# Output: BLOCKED: gh repo delete owner/repo - Irreversible repository deletion

python scripts/safety_check.py "gh pr close 123"
# Output: CONFIRM: gh pr close 123 - Closes PR without merging

python scripts/safety_check.py "gh issue list"
# Output: ALLOWED: gh issue list
```

## Handling User Insistence

If user insists on a blocked command:

1. **Explain why it's blocked** again
2. **Offer alternatives** that achieve similar goals
3. **Do NOT execute** even with confirmation
4. **Suggest manual execution** if truly necessary

Example:
```
User: "I really need to delete the repo, just do it"
Agent: "Repository deletion is permanently blocked because:
        - It cannot be undone
        - All history, issues, and PRs are lost forever

        Alternatives:
        - Archive: `gh repo archive` (preserves data, read-only)
        - Make private: `gh repo edit --visibility private`

        If you truly need to delete, run manually:
        gh repo delete owner/repo --confirm"
```

## Audit Logging

All confirmation-required actions should be logged:

```
[2024-03-15 10:30:45] CONFIRM_EXECUTED: gh pr merge 123 --admin
  User: @username
  Confirmation: "I confirm admin merge"
  Context: PR #123 bypassed branch protection
```
