from dataclasses import dataclass
from typing import List, Optional


@dataclass
class RepoSummary:
    root: str
    branch: str
    commit: str
    inside_working_tree: bool


@dataclass
class StatusSummary:
    modified: int
    staged: int
    untracked: int
    paths: List[str]


@dataclass
class CommitEntry:
    sha: str
    author: str
    date: str
    subject: str


@dataclass
class BranchInfo:
    current: str
    branches: List[str]
    upstream: Optional[str]


@dataclass
class RemoteInfo:
    name: str
    fetch_url: Optional[str]
    push_url: Optional[str]
