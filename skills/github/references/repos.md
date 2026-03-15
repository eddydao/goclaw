# Repository Operations

Guide to GitHub repository operations via `gh` CLI.

## Viewing Repositories

```bash
# Current repo info
gh repo view

# Specific repo
gh repo view owner/repo

# View in browser
gh repo view --web

# JSON output
gh repo view --json name,description,url,defaultBranchRef
```

## Listing Repositories

```bash
# Your repos
gh repo list

# Organization repos
gh repo list org-name

# With filters
gh repo list --visibility public
gh repo list --visibility private
gh repo list --fork
gh repo list --source  # non-forks only

# Limit results
gh repo list --limit 50

# JSON output
gh repo list --json name,url,isPrivate
```

## Cloning

```bash
# Clone repo
gh repo clone owner/repo

# Clone to specific directory
gh repo clone owner/repo ./my-dir

# Clone your fork
gh repo clone repo-name
```

## Forking

```bash
# Fork repo
gh repo fork owner/repo

# Fork and clone
gh repo fork owner/repo --clone

# Fork to organization
gh repo fork owner/repo --org my-org
```

## Creating Repositories

```bash
# Create public repo
gh repo create my-repo --public

# Create private repo
gh repo create my-repo --private

# Create from template
gh repo create my-repo --template owner/template-repo

# Create with description
gh repo create my-repo --description "My project"

# Create and clone
gh repo create my-repo --clone

# Initialize with README
gh repo create my-repo --add-readme
```

## Repository Settings

```bash
# Edit description
gh repo edit --description "Updated description"

# Set homepage
gh repo edit --homepage "https://example.com"

# Enable/disable features
gh repo edit --enable-issues
gh repo edit --enable-wiki=false

# Set default branch
gh repo edit --default-branch main

# Set visibility (requires confirmation)
gh repo edit --visibility public
gh repo edit --visibility private
```

## Branches

```bash
# List branches via API
gh api repos/{owner}/{repo}/branches --jq '.[].name'

# View default branch
gh repo view --json defaultBranchRef --jq '.defaultBranchRef.name'

# Create branch (use git)
git checkout -b feature-branch
git push -u origin feature-branch
```

## Releases

```bash
# List releases
gh release list

# View release
gh release view v1.0.0

# Create release
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes..."

# Create from tag
gh release create v1.0.0 --generate-notes

# Upload assets
gh release upload v1.0.0 ./build.zip

# Download assets
gh release download v1.0.0
```

## Collaborators

```bash
# List via API
gh api repos/{owner}/{repo}/collaborators --jq '.[].login'

# Add collaborator (via API)
gh api repos/{owner}/{repo}/collaborators/username -X PUT
```

## Topics/Tags

```bash
# View topics
gh repo view --json repositoryTopics

# Set topics via API
gh api repos/{owner}/{repo}/topics -X PUT -f names='["topic1","topic2"]'
```

## Secrets (for Actions)

```bash
# List secrets
gh secret list

# Set secret
gh secret set MY_SECRET

# Set from file
gh secret set MY_SECRET < secret.txt

# Delete secret
gh secret delete MY_SECRET
```

## Archive (Caution)

```bash
# Archive repo (reversible but destructive)
gh repo archive owner/repo

# Unarchive
gh repo unarchive owner/repo
```

## Safety Notes

- `gh repo delete` is BLOCKED - irreversible
- `gh repo archive` requires confirmation
- Visibility changes require confirmation
