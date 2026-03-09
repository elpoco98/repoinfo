from typing import Optional

from .git import repo_root, current_branch, short_head, NotAGitRepositoryError
from .models import RepoSummary
from .formatters import format_repo_summary


def get_repo_summary(repo: Optional[str] = None) -> RepoSummary:
    root = repo_root(repo)
    branch = current_branch(repo)
    commit = short_head(repo)
    return RepoSummary(root=root, branch=branch, commit=commit, inside_working_tree=True)


def run(args) -> None:
    s = get_repo_summary(getattr(args, "repo", None))
    print(format_repo_summary(s))
