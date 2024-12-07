import os
import subprocess
import time
from multiprocessing import Pool
from typing import Any

import git
from colorama import Fore, Style

from .cache import cache_lint_result, get_cached_lint_result
from .config import Config
from .exceptions import CrispError
from .file_selection import select_files
from .parsing import parse_black_output, parse_ruff_output
from .pre_commit import is_pre_commit
from .reporting import print_full_report, print_short_report
from .structures import FileSelectionMode, LintResult, ReturnCode


def run_crisp(
    action: str,
    mode: FileSelectionMode,
    include: list[str],
    no_pyproject_update: bool = False,
    short: bool = False,
) -> ReturnCode:
    git_repo = get_git_repo()
    repo_dir = str(git_repo.working_tree_dir)
    current_dir = os.getcwd()

    for idx, include_path in enumerate(include):
        include_path = os.path.normpath(include_path)

        if is_pre_commit():
            include_path = os.path.join(repo_dir, include_path)
        elif include_path != os.path.abspath(include_path):
            include_path = os.path.join(current_dir, include_path)

        include_path = os.path.normpath(include_path)
        common_dir = os.path.commonpath([include_path, repo_dir])

        if common_dir != repo_dir:
            raise CrispError(
                f"{Fore.LIGHTYELLOW_EX}{include_path}{Style.RESET_ALL} "
                "is outside the current Git repo."
            )
        include[idx] = include_path

    os.chdir(repo_dir)
    pyproject_toml_path = os.path.join(repo_dir, "pyproject.toml")

    if action == "init":
        Config.init(pyproject_toml_path)

        return ReturnCode.no_error

    no_pyproject_update = no_pyproject_update or is_pre_commit()

    Config.init(pyproject_toml_path, no_pyproject_update)
    files = select_files(git_repo, mode, include)

    if not files:
        print(f"{Fore.LIGHTYELLOW_EX}No files to check.")

        return ReturnCode.no_error

    results = [get_cached_lint_result(path) for path in files]

    if action == "fix":
        results, any_fixed = fix(results)
        errored_results = [r for r in results if r.errors]

        if not errored_results:
            if any_fixed:
                print(f"{Fore.LIGHTGREEN_EX}All the errors have been fixed!\n")
                print(f"{Fore.LIGHTYELLOW_EX}Do not forget to stage the fixed files.")
            else:
                print(f"{Fore.LIGHTGREEN_EX}All good, no errors to fix!")

            rc = ReturnCode.no_error
        else:
            if not any_fixed:
                print(f"{Fore.LIGHTYELLOW_EX}No automatic fixes available.\n")
            else:
                print(f"{Fore.LIGHTYELLOW_EX}Do not forget to stage the fixed files.\n")

            print_short_report(errored_results)
            rc = ReturnCode.lint_error
    else:
        results = lint(results)
        errored_results = [r for r in results if r.errors or r.needs_black]

        if not errored_results:
            print(f"{Fore.LIGHTGREEN_EX}All good!")
            rc = ReturnCode.no_error
        else:
            if short:
                print_short_report(errored_results)
            else:
                print_full_report(errored_results)

            rc = ReturnCode.lint_error

    for result in results:
        cache_lint_result(result)

    return rc


def get_git_repo() -> git.Repo:
    current_dir = os.getcwd()
    try:
        repo = git.Repo(current_dir, search_parent_directories=True)
    except git.InvalidGitRepositoryError as err:
        raise CrispError(
            f"Could not find a Git repo in "
            f"{Fore.LIGHTYELLOW_EX}{current_dir}{Style.RESET_ALL} or its parents.\n"
            f"Crisp only works in Git repos with {Fore.LIGHTYELLOW_EX}pyproject.toml"
            f"{Style.RESET_ALL} file."
        ) from err

    if repo.bare:
        raise CrispError("Bare Git repos are not supported.")

    return repo


def partition(items: list[Any], min_partition_size: int = 4) -> list[list[Any]]:
    size = max(
        min_partition_size,
        (len(items) - 1) // len(os.sched_getaffinity(os.getpid())) + 1,
    )
    num_partitions = (len(items) - 1) // size + 1
    return [items[i * size : (i + 1) * size] for i in range(num_partitions)]


def lint(results: list[LintResult]) -> list[LintResult]:
    cached = [r for r in results if r.cached]
    uncached = [r for r in results if not r.cached]

    if not uncached:
        return cached

    if is_pre_commit():
        return lint_sequential(uncached) + cached

    partitions = partition(uncached)

    if len(partitions) == 1:
        return lint_sequential(uncached) + cached
    else:
        with Pool(len(partitions)) as pool:
            updated_results = pool.map(lint_sequential, partitions)

        return [r for r_p in updated_results for r in r_p] + cached


def fix(results: list[LintResult]) -> tuple[list[LintResult], bool]:
    fixable = [r for r in results if not r.known_unfixable]
    unfixable = [r for r in results if r.known_unfixable]

    if not fixable:
        return unfixable, False

    fixable_paths = [r.path for r in fixable]

    if is_pre_commit():
        fixed_flags = fix_sequential(fixable_paths)
    else:
        partitions = partition(fixable_paths)

        if len(partitions) == 1:
            fixed_flags = fix_sequential(fixable_paths)
        else:
            with Pool(len(partitions)) as pool:
                fixed_flags = pool.map(fix_sequential, partitions)

            fixed_flags = [f for f_p in fixed_flags for f in f_p]

    for result, is_fixed in zip(fixable, fixed_flags):
        if is_fixed:
            result.just_fixed = True

    results_to_relint = [r for r in fixable if r.just_fixed or not r.cached]
    unchanged = [r for r in fixable if r.cached and not r.just_fixed]

    for result in fixable:
        result.known_unfixable = True
        result.cached = False

    if results_to_relint:
        now = time.time()

        for result in results_to_relint:
            result.check_time = now
            result.errors = []
            result.needs_black = False

        relinted = lint(results_to_relint)
        results_to_report = [r for r in relinted if r.just_fixed]

        if results_to_report:
            for r in sorted(results_to_report, key=lambda r: r.path):
                num_errors = len(r.errors)
                if num_errors == 0:
                    print(f"Fixed {Fore.LIGHTYELLOW_EX}{r.path}")
                else:
                    errors_word = "errors" if num_errors > 1 else "error"
                    print(
                        f"Partially fixed {Fore.LIGHTYELLOW_EX}{r.path} "
                        f"{Fore.LIGHTRED_EX}({num_errors} {errors_word} remaining)"
                    )
            print()

        return unfixable + unchanged + relinted, bool(results_to_report)
    else:
        return unfixable + unchanged, False


def lint_sequential(results: list[LintResult]) -> list[LintResult]:
    from .pycodestyle import run_pycodestyle

    paths = [r.path for r in results]

    ruff_proc = subprocess.Popen(
        ["ruff", "check", "--output-format", "json", *paths],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    black_proc = subprocess.Popen(
        ["black", "--check", *paths],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    run_pycodestyle(results)

    ruff_stdout, _ = ruff_proc.communicate()
    _, black_stderr = black_proc.communicate()

    if ruff_proc.returncode != 0:
        parse_ruff_output(ruff_stdout, results)

    if black_proc.returncode != 0:
        parse_black_output(black_stderr, results)

    return results


def fix_sequential(paths: list[str]) -> list[bool]:
    modified_times = {path: os.stat(path).st_mtime for path in paths}

    _ruff_proc = subprocess.run(
        ["ruff", "check", "--fix-only", *paths], capture_output=True, text=True
    )
    _black_proc = subprocess.run(["black", *paths], capture_output=True, text=True)

    fixed = [os.stat(path).st_mtime > modified_times[path] for path in paths]
    return fixed
