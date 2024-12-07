import argparse
import sys

from colorama import Fore, Style

import crisp

from .core import run_crisp
from .exceptions import CrispError
from .structures import FileSelectionMode, ReturnCode


def validate_mode(args: dict) -> FileSelectionMode:
    already_specified_an_option = False
    mode = FileSelectionMode.default

    for mode_str in ["modified", "latest_commit", "diff_main", "all_files"]:
        if args[mode_str] is True:
            if already_specified_an_option:
                raise CrispError(
                    "Specifying more than one file selection option is not allowed."
                )

            already_specified_an_option = True
            mode = FileSelectionMode[mode_str]

    return mode


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            f"{Fore.LIGHTYELLOW_EX}Coding Rules at ISP "
            f"(v{crisp.__version__}){Style.RESET_ALL}"
        )
    )
    parser.add_argument(
        "action",
        default="lint",
        const="lint",
        nargs="?",
        choices=["init", "lint", "fix"],
        help=(
            "action (set up pyproject.toml, check or fix the files); "
            "default: %(default)s"
        ),
    )
    parser.add_argument(
        "--no-pyproject-update",
        action="store_true",
        help="do not try to update pyproject.toml",
    )
    parser.add_argument("--short", action="store_true", help="print shorter report")
    parser.add_argument(
        "include",
        metavar="PATHS",
        nargs="*",
        help="check only these files (an extra filter to a File selection option)",
    )

    group = parser.add_argument_group(
        title="File selection options",
        description="Default behavior (no option specified): check uncommitted files",
    )
    group.add_argument(
        "-m",
        "--modified",
        action="store_true",
        help="check modified files only (those not fully staged)",
    )
    group.add_argument(
        "-1",
        "--latest-commit",
        action="store_true",
        help="check files affected by the latest commit",
    )
    group.add_argument(
        "--diff-main",
        action="store_true",
        help="check files from diff between default branch and the latest commit",
    )
    group.add_argument(
        "-a", "--all-files", action="store_true", help="check all files tracked by Git"
    )

    args = vars(parser.parse_args())

    try:
        mode = validate_mode(args)
        sys.exit(
            run_crisp(
                args["action"],
                mode,
                args["include"],
                args["no_pyproject_update"],
                args["short"],
            )
        )
    except CrispError as err:
        print(
            f"{Fore.LIGHTRED_EX}[{err.__class__.__name__}]{Style.RESET_ALL} {err}",
            file=sys.stderr,
        )
        sys.exit(ReturnCode.other_error)
