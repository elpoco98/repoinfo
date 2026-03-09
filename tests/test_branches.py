import os
import sys
import subprocess

# Make sure src/ is on sys.path so tests can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from git_repo_info.branches import get_branches


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_branches_listing(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    (repo / "a.txt").write_text("x")
    run(["git", "add", "a.txt"], cwd=repo)
    run(["git", "commit", "-m", "init"], cwd=repo)
    run(["git", "checkout", "-b", "branch1"], cwd=repo)
    run(["git", "checkout", "-b", "branch2"], cwd=repo)
    info = get_branches(str(repo))
    assert info.current == "branch2"
    assert "branch1" in info.branches
    assert "branch2" in info.branches
