# GitHub Actions / CI

Guide to GitHub Actions monitoring and management via `gh` CLI.

## Listing Workflow Runs

```bash
# Recent runs
gh run list

# Filter by workflow
gh run list --workflow build.yml
gh run list --workflow "CI"

# Filter by branch
gh run list --branch main
gh run list --branch feature-x

# Filter by status
gh run list --status success
gh run list --status failure
gh run list --status in_progress

# Limit results
gh run list --limit 20

# JSON output
gh run list --json databaseId,displayTitle,status,conclusion,headBranch
```

## Viewing Run Details

```bash
# View run summary
gh run view 12345

# View in browser
gh run view 12345 --web

# Exit with run's exit code (for scripting)
gh run view 12345 --exit-status

# JSON output
gh run view 12345 --json status,conclusion,jobs
```

## Logs

```bash
# View full logs
gh run view 12345 --log

# View failed job logs only
gh run view 12345 --log-failed

# Download logs
gh run download 12345

# View specific job logs
gh run view 12345 --job "Build" --log
```

## Re-running Workflows

```bash
# Rerun all jobs
gh run rerun 12345

# Rerun failed jobs only
gh run rerun 12345 --failed

# Rerun specific job
gh run rerun 12345 --job "Test"
```

## Cancelling Runs

```bash
# Cancel in-progress run
gh run cancel 12345
```

## Waiting for Completion

```bash
# Wait for run to finish
gh run watch 12345

# Script: wait and check status
gh run view 12345 --exit-status
echo "Exit code: $?"
```

## Workflow Management

```bash
# List workflows
gh workflow list

# View workflow
gh workflow view build.yml

# Enable workflow
gh workflow enable build.yml

# Disable workflow (requires confirmation)
gh workflow disable build.yml

# Run workflow manually
gh workflow run build.yml

# Run with inputs
gh workflow run build.yml -f environment=staging
```

## Artifacts

```bash
# Download artifacts from run
gh run download 12345

# Download specific artifact
gh run download 12345 --name build-output

# Download to specific directory
gh run download 12345 --dir ./artifacts
```

## Common CI Workflows

### Check PR Status
```bash
# Get latest run for current branch
gh run list --branch $(git branch --show-current) --limit 1

# View checks for a PR
gh pr checks 123
```

### Debug Failed Build
```bash
# 1. Find failed run
gh run list --status failure --limit 5

# 2. View failed logs
gh run view 12345 --log-failed

# 3. Rerun after fix
gh run rerun 12345 --failed
```

### Wait for CI Before Merge
```bash
# Watch run until complete
gh run watch 12345

# Or use auto-merge
gh pr merge 123 --auto --squash
```

## Caching

```bash
# List caches
gh cache list

# Delete cache
gh cache delete <key>
```

## Using the Script

For advanced monitoring, use the provided script:

```bash
# List with formatting
python scripts/workflow_status.py list --limit 5

# Wait with timeout
python scripts/workflow_status.py wait --run-id 12345 --timeout 300

# Rerun failed only
python scripts/workflow_status.py rerun --run-id 12345 --failed-only

# Get logs
python scripts/workflow_status.py logs --run-id 12345 --failed
```
