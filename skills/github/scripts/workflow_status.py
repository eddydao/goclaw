"""GitHub Actions monitoring and management.

Usage:
    python workflow_status.py list [--workflow name] [--branch main] [--limit 10]
    python workflow_status.py wait --run-id 123 [--timeout 600]
    python workflow_status.py rerun --run-id 123 [--failed-only]
    python workflow_status.py logs --run-id 123 [--job name]

Examples:
    # List recent workflow runs
    python workflow_status.py list --limit 5

    # Wait for a run to complete
    python workflow_status.py wait --run-id 12345 --timeout 300

    # Rerun failed jobs only
    python workflow_status.py rerun --run-id 12345 --failed-only

    # Get logs for a specific job
    python workflow_status.py logs --run-id 12345 --failed
"""

import argparse
import json
import subprocess
import sys
import time
from typing import Optional


def run_gh(args: list[str], repo: Optional[str] = None, timeout: int = 60) -> tuple[str, str, int]:
    """Run gh command, return (stdout, stderr, returncode)."""
    cmd = ["gh"] + args
    if repo:
        cmd.extend(["--repo", repo])
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", f"Command timed out after {timeout}s", 1


def cmd_list(args):
    """List workflow runs."""
    list_args = ["run", "list", "--json", "databaseId,displayTitle,status,conclusion,headBranch,createdAt,workflowName"]

    if args.workflow:
        list_args.extend(["--workflow", args.workflow])
    if args.branch:
        list_args.extend(["--branch", args.branch])
    if args.limit:
        list_args.extend(["--limit", str(args.limit)])

    stdout, stderr, code = run_gh(list_args, args.repo)

    if code != 0:
        print(f"Error listing runs: {stderr}", file=sys.stderr)
        sys.exit(1)

    runs = json.loads(stdout) if stdout.strip() else []

    if not runs:
        print("No workflow runs found.")
        return

    print(f"Recent workflow runs:\n")
    for run in runs:
        status = run.get("conclusion") or run.get("status", "unknown")
        icon = {"success": "+", "failure": "X", "cancelled": "-", "in_progress": "~"}.get(status, "?")
        print(f"[{icon}] #{run['databaseId']} {run['workflowName']}")
        print(f"    {run['displayTitle'][:60]}")
        print(f"    Branch: {run['headBranch']} | Status: {status}")
        print()


def cmd_wait(args):
    """Wait for a workflow run to complete."""
    print(f"Waiting for run #{args.run_id} to complete...")

    start_time = time.time()

    while True:
        elapsed = time.time() - start_time
        if elapsed > args.timeout:
            print(f"\nTimeout after {args.timeout}s")
            sys.exit(1)

        view_args = ["run", "view", str(args.run_id), "--json", "status,conclusion,displayTitle"]
        stdout, stderr, code = run_gh(view_args, args.repo)

        if code != 0:
            print(f"Error checking run: {stderr}", file=sys.stderr)
            sys.exit(1)

        run = json.loads(stdout)
        status = run.get("status", "unknown")
        conclusion = run.get("conclusion")

        if status == "completed":
            icon = {"success": "+", "failure": "X", "cancelled": "-"}.get(conclusion, "?")
            print(f"\n[{icon}] Run completed: {conclusion}")
            print(f"    {run['displayTitle']}")
            sys.exit(0 if conclusion == "success" else 1)

        print(f"  Status: {status} ({int(elapsed)}s elapsed)", end="\r")
        time.sleep(10)


def cmd_rerun(args):
    """Rerun a workflow."""
    rerun_args = ["run", "rerun", str(args.run_id)]

    if args.failed_only:
        rerun_args.append("--failed")

    stdout, stderr, code = run_gh(rerun_args, args.repo)

    if code == 0:
        mode = "failed jobs" if args.failed_only else "all jobs"
        print(f"Rerun triggered for run #{args.run_id} ({mode})")
    else:
        print(f"Error rerunning: {stderr}", file=sys.stderr)
        sys.exit(1)


def cmd_logs(args):
    """View logs for a workflow run."""
    log_args = ["run", "view", str(args.run_id)]

    if args.failed:
        log_args.append("--log-failed")
    elif args.job:
        log_args.extend(["--job", args.job, "--log"])
    else:
        log_args.append("--log")

    stdout, stderr, code = run_gh(log_args, args.repo)

    if code == 0:
        print(stdout)
    else:
        print(f"Error fetching logs: {stderr}", file=sys.stderr)
        sys.exit(1)


def cmd_cancel(args):
    """Cancel a workflow run."""
    cancel_args = ["run", "cancel", str(args.run_id)]

    stdout, stderr, code = run_gh(cancel_args, args.repo)

    if code == 0:
        print(f"Run #{args.run_id} cancelled")
    else:
        print(f"Error cancelling run: {stderr}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Actions monitoring",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--repo", "-R", help="Repository (owner/repo)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # list subcommand
    list_parser = subparsers.add_parser("list", help="List workflow runs")
    list_parser.add_argument("--workflow", "-w", help="Filter by workflow name")
    list_parser.add_argument("--branch", "-b", help="Filter by branch")
    list_parser.add_argument("--limit", "-l", type=int, default=10, help="Max results")
    list_parser.set_defaults(func=cmd_list)

    # wait subcommand
    wait_parser = subparsers.add_parser("wait", help="Wait for run to complete")
    wait_parser.add_argument("--run-id", "-r", required=True, type=int, help="Run ID")
    wait_parser.add_argument("--timeout", "-t", type=int, default=600, help="Timeout in seconds")
    wait_parser.set_defaults(func=cmd_wait)

    # rerun subcommand
    rerun_parser = subparsers.add_parser("rerun", help="Rerun workflow")
    rerun_parser.add_argument("--run-id", "-r", required=True, type=int, help="Run ID")
    rerun_parser.add_argument("--failed-only", "-f", action="store_true", help="Rerun failed jobs only")
    rerun_parser.set_defaults(func=cmd_rerun)

    # logs subcommand
    logs_parser = subparsers.add_parser("logs", help="View run logs")
    logs_parser.add_argument("--run-id", "-r", required=True, type=int, help="Run ID")
    logs_parser.add_argument("--job", "-j", help="Specific job name")
    logs_parser.add_argument("--failed", "-f", action="store_true", help="Show failed job logs only")
    logs_parser.set_defaults(func=cmd_logs)

    # cancel subcommand
    cancel_parser = subparsers.add_parser("cancel", help="Cancel workflow run")
    cancel_parser.add_argument("--run-id", "-r", required=True, type=int, help="Run ID")
    cancel_parser.set_defaults(func=cmd_cancel)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
