import subprocess
import shutil
from typing import List, Optional, Dict


class GitError(Exception):
    pass


class GitNotFoundError(GitError):
    pass


class NotAGitRepositoryError(GitError):
    pass


class GitCommandError(GitError):
    def __init__(self, message: str, returncode: int = 1, stderr: str = ""):
        super().__init__(message)
        self.returncode = returncode
        self.stderr = stderr


def _ensure_git_available() -> None:
    if shutil.which("git") is None:
        raise GitNotFoundError("Git executable not found in PATH")


def run_git(args: List[str], repo: Optional[str] = None, check: bool = False) -> subprocess.CompletedProcess:
    _ensure_git_available()
    cmd = ["git"] + args
    proc = subprocess.run(cmd, cwd=repo, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if check and proc.returncode != 0:
        stderr = proc.stderr.strip()
        if "not a git repository" in stderr.lower():
            raise NotAGitRepositoryError(stderr)
        raise GitCommandError(f"Git command failed: {' '.join(cmd)}", proc.returncode, stderr)
    return proc


def repo_root(repo: Optional[str] = None) -> str:
    proc = run_git(["rev-parse", "--show-toplevel"], repo=repo)
    if proc.returncode != 0:
        raise NotAGitRepositoryError(proc.stderr.strip())
    return proc.stdout.strip()


def current_branch(repo: Optional[str] = None) -> str:
    proc = run_git(["symbolic-ref", "--short", "HEAD"], repo=repo)
    if proc.returncode == 0:
        return proc.stdout.strip()
    return "DETACHED"


def short_head(repo: Optional[str] = None) -> str:
    proc = run_git(["rev-parse", "--short", "HEAD"], repo=repo)
    if proc.returncode != 0:
        raise GitCommandError("Unable to resolve HEAD", proc.returncode, proc.stderr.strip())
    return proc.stdout.strip()


def status_porcelain(repo: Optional[str] = None) -> List[str]:
    proc = run_git(["status", "--porcelain"], repo=repo)
    if proc.returncode != 0:
        stderr = proc.stderr.strip()
        if "not a git repository" in stderr.lower():
            raise NotAGitRepositoryError(stderr)
        raise GitCommandError("git status failed", proc.returncode, stderr)
    out = proc.stdout
    return [line for line in out.splitlines() if line.strip() != ""]


def log_pretty(n: int = 10, repo: Optional[str] = None) -> str:
    fmt = "%h%x1f%an%x1f%ad%x1f%s"
    proc = run_git(["log", f"--pretty=format:{fmt}", "--date=iso", f"-n{n}"], repo=repo)
    if proc.returncode != 0:
        raise GitCommandError("git log failed", proc.returncode, proc.stderr.strip())
    return proc.stdout


def list_branches(repo: Optional[str] = None) -> List[str]:
    proc = run_git(["for-each-ref", "--format=%(refname:short)", "refs/heads/"], repo=repo)
    if proc.returncode != 0:
        raise GitCommandError("git branch listing failed", proc.returncode, proc.stderr.strip())
    return [line for line in proc.stdout.splitlines() if line.strip()]


def remotes(repo: Optional[str] = None) -> List[Dict[str, str]]:
    proc = run_git(["remote", "-v"], repo=repo)
    if proc.returncode != 0:
        raise GitCommandError("git remote -v failed", proc.returncode, proc.stderr.strip())
    remotes: Dict[str, Dict[str, str]] = {}
    for line in proc.stdout.splitlines():
        parts = line.split()
        if len(parts) >= 3:
            name, url, typ = parts[0], parts[1], parts[2].strip("()")
            remotes.setdefault(name, {})[typ] = url
    return [{"name": name, "fetch_url": urls.get("fetch"), "push_url": urls.get("push")} for name, urls in remotes.items()]
