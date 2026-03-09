"""Log command implementation."""

from typing import Optional, List
from .git import log_pretty
from .models import CommitEntry
from .formatters import format_commit_list


def get_commits(n: int = 10, repo: Optional[str] = None) -> List[CommitEntry]:
    """Return the most recent n commits as CommitEntry objects."""
    out = log_pretty(n=n, repo=repo)
    commits: List[CommitEntry] = []
    for line in out.splitlines():
        if not line.strip():
            continue
        parts = line.split("\x1f")
        if len(parts) >= 4:
            sha, author, date, subject = parts[0], parts[1], parts[2], parts[3]
            commits.append(CommitEntry(sha=sha, author=author, date=date, subject=subject))
    return commits


def run(args) -> None:
    repo = getattr(args, "repo", None)
    n = getattr(args, "number", 10)
    commits = get_commits(n=n, repo=repo)
    print(format_commit_list(commits))
