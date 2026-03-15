"""PR lifecycle management for GitHub.

Usage:
    python pr_workflow.py create --branch feat/x --title "Add X" [--draft] [--base main]
    python pr_workflow.py review --pr 123 --approve [--body "LGTM"]
    python pr_workflow.py merge --pr 123 [--squash|--rebase|--merge]
    python pr_workflow.py status --pr 123
    python pr_workflow.py list [--state open] [--author @me]

Examples:
    # Create a PR from current branch
    python pr_workflow.py create --title "Add feature X" --body "Description"

    # Approve a PR
    python pr_workflow.py review --pr 123 --approve --body "LGTM!"

    # Merge with squash
    python pr_workflow.py merge --pr 123 --squash
"""

import argparse
import json
import subprocess
import sys
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


def cmd_create(args):
    """Create a new pull request."""
    create_args = ["pr", "create"]

    if args.title:
        create_args.extend(["--title", args.title])
    if args.body:
        create_args.extend(["--body", args.body])
    if args.base:
        create_args.extend(["--base", args.base])
    if args.draft:
        create_args.append("--draft")
    if args.reviewer:
        create_args.extend(["--reviewer", args.reviewer])
    if args.assignee:
        create_args.extend(["--assignee", args.assignee])
    if args.label:
        create_args.extend(["--label", args.label])

    stdout, stderr, code = run_gh(create_args, args.repo)

    if code == 0:
        print(f"PR created: {stdout.strip()}")
    else:
        print(f"Error creating PR: {stderr}", file=sys.stderr)
        sys.exit(1)


def cmd_review(args):
    """Review a pull request."""
    review_args = ["pr", "review", str(args.pr)]

    if args.approve:
        review_args.append("--approve")
    elif args.request_changes:
        review_args.append("--request-changes")
    elif args.comment:
        review_args.append("--comment")

    if args.body:
        review_args.extend(["--body", args.body])

    stdout, stderr, code = run_gh(review_args, args.repo)

    if code == 0:
        action = "approved" if args.approve else "reviewed"
        print(f"PR #{args.pr} {action}")
    else:
        print(f"Error reviewing PR: {stderr}", file=sys.stderr)
        sys.exit(1)


def cmd_merge(args):
    """Merge a pull request."""
    merge_args = ["pr", "merge", str(args.pr)]

    if args.squash:
        merge_args.append("--squash")
    elif args.rebase:
        merge_args.append("--rebase")
    elif args.merge:
        merge_args.append("--merge")

    if args.auto:
        merge_args.append("--auto")

    if args.delete_branch:
        merge_args.append("--delete-branch")

    stdout, stderr, code = run_gh(merge_args, args.repo)

    if code == 0:
        print(f"PR #{args.pr} merged successfully")
    else:
        print(f"Error merging PR: {stderr}", file=sys.stderr)
        sys.exit(1)


def cmd_status(args):
    """Show PR status including checks."""
    # Get PR details
    view_args = ["pr", "view", str(args.pr), "--json",
                 "number,title,state,author,baseRefName,headRefName,mergeable,reviewDecision,statusCheckRollup"]

    stdout, stderr, code = run_gh(view_args, args.repo)

    if code != 0:
        print(f"Error fetching PR: {stderr}", file=sys.stderr)
        sys.exit(1)

    pr = json.loads(stdout)

    print(f"PR #{pr['number']}: {pr['title']}")
    print(f"  State: {pr['state']}")
    print(f"  Author: {pr['author']['login']}")
    print(f"  Branch: {pr['headRefName']} -> {pr['baseRefName']}")
    print(f"  Mergeable: {pr.get('mergeable', 'unknown')}")
    print(f"  Review: {pr.get('reviewDecision', 'none')}")

    checks = pr.get("statusCheckRollup", [])
    if checks:
        print(f"\n  Checks ({len(checks)}):")
        for check in checks:
            status = check.get("conclusion") or check.get("status", "pending")
            name = check.get("name", "unknown")
            print(f"    [{status:10}] {name}")


def cmd_list(args):
    """List pull requests."""
    list_args = ["pr", "list", "--json", "number,title,state,author,headRefName,createdAt"]

    if args.state:
        list_args.extend(["--state", args.state])
    if args.author:
        list_args.extend(["--author", args.author])
    if args.limit:
        list_args.extend(["--limit", str(args.limit)])

    stdout, stderr, code = run_gh(list_args, args.repo)

    if code != 0:
        print(f"Error listing PRs: {stderr}", file=sys.stderr)
        sys.exit(1)

    prs = json.loads(stdout) if stdout.strip() else []

    if not prs:
        print("No PRs found.")
        return

    print(f"Found {len(prs)} PRs:\n")
    for pr in prs:
        author = pr.get("author", {}).get("login", "unknown")
        print(f"#{pr['number']:5} [{pr['state']:6}] {pr['title'][:50]}")
        print(f"       {pr['headRefName']} by {author}")


def main():
    parser = argparse.ArgumentParser(
        description="PR lifecycle management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--repo", "-R", help="Repository (owner/repo)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # create subcommand
    create_parser = subparsers.add_parser("create", help="Create a PR")
    create_parser.add_argument("--title", "-t", help="PR title")
    create_parser.add_argument("--body", "-b", help="PR body")
    create_parser.add_argument("--base", help="Base branch")
    create_parser.add_argument("--draft", "-d", action="store_true", help="Create as draft")
    create_parser.add_argument("--reviewer", "-r", help="Request reviewer")
    create_parser.add_argument("--assignee", "-a", help="Assign to user")
    create_parser.add_argument("--label", "-l", help="Add label")
    create_parser.set_defaults(func=cmd_create)

    # review subcommand
    review_parser = subparsers.add_parser("review", help="Review a PR")
    review_parser.add_argument("--pr", "-p", required=True, type=int, help="PR number")
    review_action = review_parser.add_mutually_exclusive_group(required=True)
    review_action.add_argument("--approve", action="store_true", help="Approve PR")
    review_action.add_argument("--request-changes", action="store_true", help="Request changes")
    review_action.add_argument("--comment", action="store_true", help="Comment only")
    review_parser.add_argument("--body", "-b", help="Review body")
    review_parser.set_defaults(func=cmd_review)

    # merge subcommand
    merge_parser = subparsers.add_parser("merge", help="Merge a PR")
    merge_parser.add_argument("--pr", "-p", required=True, type=int, help="PR number")
    merge_parser.add_argument("--squash", "-s", action="store_true", help="Squash merge")
    merge_parser.add_argument("--rebase", "-r", action="store_true", help="Rebase merge")
    merge_parser.add_argument("--merge", "-m", action="store_true", help="Merge commit")
    merge_parser.add_argument("--auto", action="store_true", help="Auto-merge when ready")
    merge_parser.add_argument("--delete-branch", "-d", action="store_true", help="Delete branch after merge")
    merge_parser.set_defaults(func=cmd_merge)

    # status subcommand
    status_parser = subparsers.add_parser("status", help="Show PR status")
    status_parser.add_argument("--pr", "-p", required=True, type=int, help="PR number")
    status_parser.set_defaults(func=cmd_status)

    # list subcommand
    list_parser = subparsers.add_parser("list", help="List PRs")
    list_parser.add_argument("--state", "-s", choices=["open", "closed", "merged", "all"], default="open")
    list_parser.add_argument("--author", "-a", help="Filter by author")
    list_parser.add_argument("--limit", "-l", type=int, default=30, help="Max results")
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
