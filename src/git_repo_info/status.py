"""Status command implementation."""

from typing import Optional, List
from .git import status_porcelain
from .models import StatusSummary
from .formatters import format_status_summary


def get_status_summary(repo: Optional[str] = None) -> StatusSummary:
    """Parse `git status --porcelain` output and return summary counts and paths."""
    lines = status_porcelain(repo)
    modified = 0
    staged = 0
    untracked = 0
    paths: List[str] = []
    for line in lines:
        if line.startswith("??"):
            untracked += 1
            path = line[3:].strip()
            paths.append(path)
        else:
            x = line[0] if len(line) > 0 else " "
            y = line[1] if len(line) > 1 else " "
            path = line[3:].strip() if len(line) > 3 else line.strip()
            if x != " ":
                staged += 1
            if y != " ":
                modified += 1
            paths.append(path)
    return StatusSummary(modified=modified, staged=staged, untracked=untracked, paths=paths)


def run(args) -> None:
    repo = getattr(args, "repo", None)
    show_paths = getattr(args, "paths", False)
    summary = get_status_summary(repo)
    if not show_paths:
        summary = StatusSummary(modified=summary.modified, staged=summary.staged, untracked=summary.untracked, paths=[])
    print(format_status_summary(summary))
