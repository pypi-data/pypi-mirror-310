import os

import git
from colorama import Fore, Style
from wcmatch import glob

from .config import Config
from .exceptions import CrispError
from .pre_commit import is_pre_commit
from .structures import ExcludePatternKind, FileSelectionMode

EMPTY_TREE_SHA = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"


def select_files(
    git_repo: git.Repo, mode: FileSelectionMode, include: list[str]
) -> list[str]:
    def _from_working_tree(include_staged):
        if include_staged:
            against = "HEAD" if git_repo.head.is_valid() else EMPTY_TREE_SHA

            return git_repo.git.diff(against, name_only=True)
        else:
            return git_repo.git.diff(None, name_only=True)

    def _from_commit_diff(branch):
        if not git_repo.head.is_valid():
            raise CrispError(
                "Repo "
                f"{Fore.LIGHTYELLOW_EX}{git_repo.working_tree_dir}{Style.RESET_ALL} "
                "has no commits."
            )

        if not git_repo.head.commit.parents:
            against = EMPTY_TREE_SHA
        elif branch is not None:
            against = branch
        else:
            against = "HEAD~1"

        return git_repo.git.diff(f"{against}..HEAD", name_only=True)

    if mode == FileSelectionMode.default:
        git_files = _from_working_tree(include_staged=True)
    elif mode == FileSelectionMode.modified:
        git_files = _from_working_tree(include_staged=False)
    elif mode == FileSelectionMode.latest_commit:
        git_files = _from_commit_diff(branch=None)
    elif mode == FileSelectionMode.diff_main:
        git_files = _from_commit_diff(branch=Config().default_branch)
    else:
        git_files = git_repo.git.ls_files()

    git_files = git_files.split("\n")
    workdir = os.getcwd()

    patterns = [
        ExcludePattern(pattern, ExcludePatternKind.exclude, workdir=workdir)
        for pattern in Config().exclude
    ]
    if include:
        patterns += [
            ExcludePattern(full_path, ExcludePatternKind.include, workdir=workdir)
            for full_path in include
        ]
    else:
        patterns += [ExcludePattern("**", ExcludePatternKind.include, workdir=workdir)]

    return exclude_files(
        [f for f in git_files if os.path.isfile(f)],
        patterns,
        force_exclude=is_pre_commit(),
    )


class ExcludePattern:
    def __init__(
        self, raw_pattern: str, kind: ExcludePatternKind, workdir: str
    ) -> None:
        self.kind = kind

        is_directory = raw_pattern.endswith(os.path.sep)
        no_trailing_slash = raw_pattern.rstrip(os.path.sep)

        is_path = os.path.sep in no_trailing_slash or no_trailing_slash in [
            "**",
            ".",
            "..",
        ]

        if kind == ExcludePatternKind.include:
            relpath = os.path.relpath(raw_pattern, start=workdir)
        else:
            if is_path:
                relpath = raw_pattern.lstrip(os.path.sep)
            else:
                relpath = os.path.join("**", raw_pattern)
            relpath = os.path.normpath(relpath)

        if relpath == ".":
            relpath = "**"

        if relpath.endswith("**"):
            self.pattern = relpath
        else:
            with_globstar = os.path.join(relpath, "**")

            if is_directory:
                self.pattern = with_globstar
            else:
                self.pattern = [with_globstar, relpath]

    def match(self, actual_file: str) -> bool:
        return glob.globmatch(actual_file, self.pattern, flags=glob.GLOBSTAR)

    def oldest_matching_parent(self, actual_file: str) -> str:
        matching_parent = actual_file

        while True:
            parent_dir = os.path.dirname(matching_parent)

            if not self.match(parent_dir + os.path.sep):
                break

            matching_parent = parent_dir

            if matching_parent == "":
                break

        return matching_parent


def exclude_files(
    files: list[str], patterns: list[ExcludePattern], force_exclude: bool = False
) -> list[str]:
    filtered_files: list[str] = []

    for file_ in files:
        if os.path.splitext(file_)[1] != ".py":
            continue

        exclude_matches: list[ExcludePattern] = []
        include_matches: list[ExcludePattern] = []

        for pattern in patterns:
            if pattern.match(file_):
                append_to = (
                    exclude_matches
                    if pattern.kind == ExcludePatternKind.exclude
                    else include_matches
                )
                append_to.append(pattern)

        if not include_matches or (exclude_matches and force_exclude):
            continue
        elif not exclude_matches:
            filtered_files.append(file_)
            continue

        most_specific_exclude = max(
            pattern.oldest_matching_parent(file_) for pattern in exclude_matches
        )
        most_specific_include = max(
            pattern.oldest_matching_parent(file_) for pattern in include_matches
        )

        if most_specific_include >= most_specific_exclude:
            filtered_files.append(file_)

    return filtered_files
