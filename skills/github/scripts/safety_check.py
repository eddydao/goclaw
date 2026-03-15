"""Validate gh/git commands before execution.

Usage:
    python safety_check.py "<full command>"

Output:
    ALLOWED: <command>
    BLOCKED: <command> - <reason>
    CONFIRM: <command> - <reason>

Exit codes:
    0 - ALLOWED
    1 - BLOCKED
    2 - CONFIRM required
"""

import re
import sys

# Blocked patterns - NEVER execute
BLOCKED_PATTERNS = [
    (r"gh\s+repo\s+delete", "Irreversible repository deletion"),
    (r"gh\s+api\s+.*DELETE\s+/repos/", "API-level repository deletion"),
    (r"git\s+push\s+--force\s+.*\b(main|master)\b", "Force push to protected branch - use --force-with-lease"),
    (r"git\s+push\s+-f\s+.*\b(main|master)\b", "Force push to protected branch - use --force-with-lease"),
    (r"gh\s+issue\s+close\s+--.*\ball\b", "Bulk close all issues without review"),
    (r"rm\s+-rf\s+/", "Dangerous filesystem deletion"),
]

# Confirmation patterns - require explicit approval
CONFIRM_PATTERNS = [
    (r"gh\s+pr\s+merge\s+.*--admin", "Bypasses branch protection rules"),
    (r"gh\s+pr\s+close", "Closes PR without merging"),
    (r"gh\s+workflow\s+disable", "Disables CI workflow"),
    (r"gh\s+release\s+delete", "Removes release permanently"),
    (r"gh\s+issue\s+close", "Closes issue"),
    (r"git\s+push\s+--force-with-lease", "Force push (safer but still destructive)"),
    (r"gh\s+repo\s+archive", "Archives repository"),
]


def check_command(command: str) -> tuple[str, str, int]:
    """Check if command is allowed, blocked, or needs confirmation.

    Returns:
        (status, message, exit_code)
    """
    cmd_lower = command.lower().strip()

    # Check blocked patterns first
    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, cmd_lower, re.IGNORECASE):
            return "BLOCKED", f"{command} - {reason}", 1

    # Check confirmation patterns
    for pattern, reason in CONFIRM_PATTERNS:
        if re.search(pattern, cmd_lower, re.IGNORECASE):
            return "CONFIRM", f"{command} - {reason}", 2

    return "ALLOWED", command, 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python safety_check.py \"<command>\"")
        print("\nExample:")
        print("  python safety_check.py \"gh repo delete owner/repo\"")
        sys.exit(1)

    command = " ".join(sys.argv[1:])
    status, message, exit_code = check_command(command)

    print(f"{status}: {message}")
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
