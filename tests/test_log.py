import os
import sys
import subprocess

# Make sure src/ is on sys.path so tests can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from git_repo_info.log import get_commits


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_log_parsing(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    (repo / "a.txt").write_text("one")
    run(["git", "add", "a.txt"], cwd=repo)
    run(["git", "commit", "-m", "first"], cwd=repo)
    (repo / "a.txt").write_text("two")
    run(["git", "add", "a.txt"], cwd=repo)
    run(["git", "commit", "-m", "second"], cwd=repo)
    commits = get_commits(2, str(repo))
    assert len(commits) == 2
    assert commits[0].subject == "second"
    assert commits[1].subject == "first"
