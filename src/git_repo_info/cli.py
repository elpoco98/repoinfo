import argparse
import sys
from typing import Optional

from . import summary, status, log as logmod, branches as branchesmod, remotes as remotesmod


def main(argv: Optional[list[str]] = None) -> None:
    parser = argparse.ArgumentParser(prog="git-repo-info")
    parser.add_argument("--repo", "-r", help="Path to repository", default=None)
    subparsers = parser.add_subparsers(dest="command")
    subparsers.required = True

    subparsers.add_parser("summary")

    status_p = subparsers.add_parser("status")
    status_p.add_argument("--paths", action="store_true", help="Show affected file paths")

    log_p = subparsers.add_parser("log")
    log_p.add_argument("-n", "--number", type=int, default=10, help="Number of commits to show")

    branches_p = subparsers.add_parser("branches")
    branches_p.add_argument("--show-upstream", action="store_true", help="Show upstream for current branch")

    subparsers.add_parser("remotes")

    args = parser.parse_args(argv)

    try:
        if args.command == "summary":
            summary.run(args)
        elif args.command == "status":
            status.run(args)
        elif args.command == "log":
            logmod.run(args)
        elif args.command == "branches":
            branchesmod.run(args)
        elif args.command == "remotes":
            remotesmod.run(args)
        else:
            print(f"Unknown command: {args.command}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
