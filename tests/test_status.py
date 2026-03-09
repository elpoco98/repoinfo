import os
import sys
import subprocess

# Make sure src/ is on sys.path so tests can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from git_repo_info.status import get_status_summary


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_status_counts(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    (repo / "a.txt").write_text("initial")
    run(["git", "add", "a.txt"], cwd=repo)
    run(["git", "commit", "-m", "init"], cwd=repo)

    # staged file
    (repo / "staged.txt").write_text("s")
    run(["git", "add", "staged.txt"], cwd=repo)
    # modified file
    (repo / "a.txt").write_text("changed")
    # untracked file
    (repo / "untracked.txt").write_text("u")

    s = get_status_summary(str(repo))
    assert s.staged == 1
    assert s.modified == 1
    assert s.untracked == 1
