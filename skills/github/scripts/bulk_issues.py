"""Bulk issue operations for GitHub.

Usage:
    python bulk_issues.py label --query "is:open no:label" --add triage [--repo owner/repo]
    python bulk_issues.py assign --query "is:open label:bug" --assignee @me [--repo owner/repo]
    python bulk_issues.py close --numbers 1,2,3 --reason completed [--repo owner/repo]
    python bulk_issues.py list --query "is:open" [--format json] [--repo owner/repo]

Examples:
    # Add triage label to unlabeled issues
    python bulk_issues.py label --query "no:label" --add triage

    # Assign all bug issues to yourself
    python bulk_issues.py assign --query "label:bug" --assignee @me

    # Close specific issues
    python bulk_issues.py close --numbers 10,11,12 --reason "duplicate"
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


def get_issues(query: str, repo: Optional[str] = None) -> list[dict]:
    """Fetch issues matching query."""
    args = ["issue", "list", "--search", query, "--json", "number,title,state,labels,assignees", "--limit", "100"]
    stdout, stderr, code = run_gh(args, repo)

    if code != 0:
        print(f"Error fetching issues: {stderr}", file=sys.stderr)
        return []

    try:
        return json.loads(stdout) if stdout.strip() else []
    except json.JSONDecodeError:
        print(f"Error parsing response: {stdout}", file=sys.stderr)
        return []


def cmd_label(args):
    """Add or remove labels from issues matching query."""
    issues = get_issues(args.query, args.repo)

    if not issues:
        print("No issues found matching query.")
        return

    print(f"Found {len(issues)} issues matching query.")

    success = 0
    errors = []

    for issue in issues:
        num = issue["number"]
        edit_args = ["issue", "edit", str(num)]

        if args.add:
            edit_args.extend(["--add-label", args.add])
        if args.remove:
            edit_args.extend(["--remove-label", args.remove])

        _, stderr, code = run_gh(edit_args, args.repo)

        if code == 0:
            success += 1
            print(f"  Updated #{num}: {issue['title'][:50]}")
        else:
            errors.append(f"#{num}: {stderr.strip()}")

    print(f"\nCompleted: {success}/{len(issues)} issues updated")
    if errors:
        print("Errors:")
        for err in errors:
            print(f"  {err}")


def cmd_assign(args):
    """Assign issues matching query to a user."""
    issues = get_issues(args.query, args.repo)

    if not issues:
        print("No issues found matching query.")
        return

    print(f"Found {len(issues)} issues matching query.")

    success = 0
    errors = []

    for issue in issues:
        num = issue["number"]
        edit_args = ["issue", "edit", str(num), "--add-assignee", args.assignee]

        _, stderr, code = run_gh(edit_args, args.repo)

        if code == 0:
            success += 1
            print(f"  Assigned #{num} to {args.assignee}")
        else:
            errors.append(f"#{num}: {stderr.strip()}")

    print(f"\nCompleted: {success}/{len(issues)} issues assigned")
    if errors:
        print("Errors:")
        for err in errors:
            print(f"  {err}")


def cmd_close(args):
    """Close specific issues by number."""
    numbers = [n.strip() for n in args.numbers.split(",")]

    print(f"Closing {len(numbers)} issues...")

    success = 0
    errors = []

    for num in numbers:
        close_args = ["issue", "close", num]
        if args.reason:
            close_args.extend(["--reason", args.reason])

        _, stderr, code = run_gh(close_args, args.repo)

        if code == 0:
            success += 1
            print(f"  Closed #{num}")
        else:
            errors.append(f"#{num}: {stderr.strip()}")

    print(f"\nCompleted: {success}/{len(numbers)} issues closed")
    if errors:
        print("Errors:")
        for err in errors:
            print(f"  {err}")


def cmd_list(args):
    """List issues matching query."""
    issues = get_issues(args.query, args.repo)

    if args.format == "json":
        print(json.dumps(issues, indent=2))
    else:
        if not issues:
            print("No issues found.")
            return

        print(f"Found {len(issues)} issues:\n")
        for issue in issues:
            labels = ", ".join(l["name"] for l in issue.get("labels", []))
            assignees = ", ".join(a["login"] for a in issue.get("assignees", []))
            print(f"#{issue['number']:5} [{issue['state']:6}] {issue['title'][:60]}")
            if labels:
                print(f"       Labels: {labels}")
            if assignees:
                print(f"       Assignees: {assignees}")


def main():
    parser = argparse.ArgumentParser(
        description="Bulk issue operations for GitHub",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("--repo", "-R", help="Repository (owner/repo)")

    subparsers = parser.add_subparsers(dest="command", required=True)

    # label subcommand
    label_parser = subparsers.add_parser("label", help="Add/remove labels from issues")
    label_parser.add_argument("--query", "-q", required=True, help="Search query")
    label_parser.add_argument("--add", "-a", help="Label to add")
    label_parser.add_argument("--remove", "-r", help="Label to remove")
    label_parser.set_defaults(func=cmd_label)

    # assign subcommand
    assign_parser = subparsers.add_parser("assign", help="Assign issues to user")
    assign_parser.add_argument("--query", "-q", required=True, help="Search query")
    assign_parser.add_argument("--assignee", "-u", required=True, help="User to assign")
    assign_parser.set_defaults(func=cmd_assign)

    # close subcommand
    close_parser = subparsers.add_parser("close", help="Close issues by number")
    close_parser.add_argument("--numbers", "-n", required=True, help="Comma-separated issue numbers")
    close_parser.add_argument("--reason", "-r", help="Close reason (completed, not_planned, duplicate)")
    close_parser.set_defaults(func=cmd_close)

    # list subcommand
    list_parser = subparsers.add_parser("list", help="List issues matching query")
    list_parser.add_argument("--query", "-q", required=True, help="Search query")
    list_parser.add_argument("--format", "-f", choices=["text", "json"], default="text", help="Output format")
    list_parser.set_defaults(func=cmd_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
