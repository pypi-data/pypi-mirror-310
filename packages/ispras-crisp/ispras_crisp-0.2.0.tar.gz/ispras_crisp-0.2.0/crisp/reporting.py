from colorama import Fore, Style

from .structures import LintResult


def print_full_report(errored_results: list[LintResult]) -> None:
    errored_results = sorted(errored_results, key=lambda r: r.path)

    for r in errored_results:
        print(f"{Fore.LIGHTYELLOW_EX}{r.path}")

        errors = sorted(r.errors, key=lambda e: (e.line, e.col))
        for e in errors:
            print(
                f"    {e.line}{Style.DIM}:{e.col}: "
                f"{Style.RESET_ALL}{Fore.LIGHTRED_EX}{e.code} "
                f"{Style.RESET_ALL}{e.msg}"
            )

        if r.needs_black:
            print(f"    {Fore.LIGHTRED_EX}needs Black reformatting")


def print_short_report(errored_results: list[LintResult]) -> None:
    num_errors = sum(len(r.errors) + int(r.needs_black) for r in errored_results)

    errors_word = "errors" if num_errors > 1 else "error"
    files_word = "files" if len(errored_results) > 1 else "file"

    print(
        f"There are still {Fore.LIGHTRED_EX}{num_errors} {errors_word} "
        f"{Style.RESET_ALL}in {Fore.LIGHTRED_EX}{len(errored_results)} "
        f"{files_word}{Style.RESET_ALL}."
    )
