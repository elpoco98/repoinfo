# git-repo-info

A small, beginner-friendly Python CLI that inspects a local Git repository and prints concise, human-readable summaries. The tool is read-only and intentionally calls the Git executable (`git`) via subprocess to stay close to the commands students learn.

Prerequisites
- Python 3.11+
- Git installed and available on PATH
- (Optional for tests) pytest.

Quick start

Run without installing the package by adding `src/` to PYTHONPATH and using the module entrypoint:

- Summary for the current directory

  PYTHONPATH=src python -m git_repo_info summary

- Inspect a different repository

  PYTHONPATH=src python -m git_repo_info summary --repo /path/to/repo

Available subcommands

- summary
  - Shows repository root, current branch (or DETACHED), short commit SHA, and whether inside a working tree.
  - Example: `PYTHONPATH=src python -m git_repo_info summary --repo /path/to/repo`

- status
  - Counts modified, staged, and untracked files (parses `git status --porcelain`).
  - Options: `--paths` to list affected file paths.
  - Example: `PYTHONPATH=src python -m git_repo_info status --paths`

- log
  - Shows recent commits using an explicit `git log --pretty=format:...` string (short SHA, author, date, subject).
  - Options: `-n` / `--number` to control how many commits to show (default 10).
  - Example: `PYTHONPATH=src python -m git_repo_info log -n 5`

- branches
  - Lists local branches and indicates the current branch.
  - Optionally shows the upstream (remote-tracking) branch for the current branch with `--show-upstream`.
  - Example: `PYTHONPATH=src python -m git_repo_info branches --show-upstream`

- remotes
  - Lists configured remotes and their fetch/push URLs.
  - Example: `PYTHONPATH=src python -m git_repo_info remotes`

Running tests

If a virtual environment is present at `.venv/` (as used in development), activate it and run pytest:

- Activate (bash)

  source .venv/bin/activate
  pytest -q

- Or run pytest directly from the venv without activating:

  .venv/bin/pytest -q

Troubleshooting
- If the tool prints an error about `git` not being found, install Git and ensure it is on PATH.
- If you get "not a git repository", verify the path passed to `--repo` contains a Git repository (a `.git` folder) or run the tool from inside a repo.
- The CLI exits with non-zero status codes on errors and prints a short diagnostic to stderr.

Developer notes
- Code is intentionally split into small, focused modules under `src/git_repo_info/`:
  - `git.py` — subprocess-based Git wrapper and errors
  - `models.py` — dataclasses describing outputs
  - `formatters.py` — rendering models to human text
  - One file per subcommand: `summary.py`, `status.py`, `log.py`, `branches.py`, `remotes.py`
  - `cli.py` — argparse wiring and dispatch
- Tests are in `tests/` and create temporary Git repositories to verify behavior.

If you'd like a packaged install (`pip install -e .`) or an executable entrypoint, a small `pyproject.toml` or `setup.cfg` can be added — say so and that can be implemented next.
