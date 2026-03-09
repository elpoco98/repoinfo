"""Remotes command implementation."""

from typing import Optional, List
from .git import remotes as git_remotes
from .models import RemoteInfo
from .formatters import format_remotes


def get_remotes(repo: Optional[str] = None) -> List[RemoteInfo]:
    raw = git_remotes(repo)
    return [RemoteInfo(name=r["name"], fetch_url=r.get("fetch_url"), push_url=r.get("push_url")) for r in raw]


def run(args) -> None:
    repo = getattr(args, "repo", None)
    r = get_remotes(repo)
    print(format_remotes(r))
