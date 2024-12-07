import json
import os

from .structures import LintError, LintResult


def parse_ruff_output(ruff_output_json: str, results: list[LintResult]) -> None:
    ruff_output = json.loads(ruff_output_json)
    results_dict = {r.path: r for r in results}
    current_dir = os.getcwd()

    for ruff_error in ruff_output:
        path = os.path.relpath(ruff_error["filename"], current_dir)
        line = ruff_error["location"]["row"]
        col = ruff_error["location"]["column"]
        code = ruff_error["code"] or "E999"
        msg = ruff_error["message"]

        error = LintError(line, col, code, msg)
        results_dict[path].errors.append(error)


def parse_black_output(black_output: str, results: list[LintResult]) -> None:
    results_dict = {r.path: r for r in results}
    current_dir = os.getcwd()

    for line in black_output.split("\n"):
        if line.startswith("would reformat "):
            path = os.path.relpath(line[len("would reformat ") :], current_dir)
            results_dict[path].needs_black = True
