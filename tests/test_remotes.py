import os
import sys
import subprocess

# Make sure src/ is on sys.path so tests can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from git_repo_info.remotes import get_remotes


def run(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)


def test_remotes_parsing(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    run(["git", "init"], cwd=repo)
    run(["git", "config", "user.email", "test@example.com"], cwd=repo)
    run(["git", "config", "user.name", "Test User"], cwd=repo)
    run(["git", "remote", "add", "origin", "https://example.com/repo.git"], cwd=repo)
    rems = get_remotes(str(repo))
    assert any(r.name == "origin" for r in rems)
    origin = [r for r in rems if r.name == "origin"][0]
    assert origin.fetch_url == "https://example.com/repo.git"
    assert origin.push_url == "https://example.com/repo.git"
