from .models import RepoSummary, StatusSummary, CommitEntry, BranchInfo, RemoteInfo
from typing import List


def format_repo_summary(s: RepoSummary) -> str:
    return (
        f"Repository root: {s.root}\n"
        f"Branch: {s.branch}\n"
        f"Commit: {s.commit}\n"
        f"Inside working tree: {s.inside_working_tree}"
    )


def format_status_summary(s: StatusSummary) -> str:
    lines: List[str] = []
    lines.append(f"Modified files: {s.modified}")
    lines.append(f"Staged files: {s.staged}")
    lines.append(f"Untracked files: {s.untracked}")
    if s.paths:
        lines.append("\nAffected paths:")
        lines.extend(s.paths)
    return "\n".join(lines)


def format_commit_list(commits: List[CommitEntry]) -> str:
    lines: List[str] = []
    for c in commits:
        lines.append(f"{c.sha} {c.author} {c.date} {c.subject}")
    return "\n".join(lines)


def format_branches(b: BranchInfo) -> str:
    lines: List[str] = []
    lines.append(f"Current branch: {b.current}")
    lines.append("Local branches:")
    lines.extend(b.branches)
    if b.upstream:
        lines.append(f"Upstream: {b.upstream}")
    return "\n".join(lines)


def format_remotes(remotes_list: List[RemoteInfo]) -> str:
    lines: List[str] = []
    for r in remotes_list:
        lines.append(f"{r.name}: fetch={r.fetch_url} push={r.push_url}")
    return "\n".join(lines)
