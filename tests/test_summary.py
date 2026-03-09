import os
import sys
import subprocess

# Make sure src/ is on sys.path so tests can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from git_repo_info.summary import get_repo_summary


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_summary_basic(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    # create and switch to a known branch to avoid relying on git defaults
    run(["git", "checkout", "-b", "test-branch"], cwd=repo)
    (repo / "a.txt").write_text("hello")
    run(["git", "add", "a.txt"], cwd=repo)
    run(["git", "commit", "-m", "init"], cwd=repo)

    summary = get_repo_summary(str(repo))
    assert summary.branch == "test-branch"
    assert os.path.abspath(summary.root) == os.path.abspath(str(repo))
    assert summary.commit != ""
