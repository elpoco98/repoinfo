"""Branches command implementation."""

from typing import Optional
from .git import list_branches, current_branch, run_git
from .models import BranchInfo
from .formatters import format_branches


def get_branches(repo: Optional[str] = None, show_upstream: bool = False) -> BranchInfo:
    branches = list_branches(repo)
    current = current_branch(repo)
    upstream = None
    if show_upstream and current != "DETACHED":
        proc = run_git(["rev-parse", "--abbrev-ref", "--symbolic-full-name", f"{current}@{{u}}"], repo=repo, check=False)
        if proc.returncode == 0:
            upstream = proc.stdout.strip()
    return BranchInfo(current=current, branches=branches, upstream=upstream)


def run(args) -> None:
    repo = getattr(args, "repo", None)
    show_upstream = getattr(args, "show_upstream", False)
    info = get_branches(repo=repo, show_upstream=show_upstream)
    print(format_branches(info))
