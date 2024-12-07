import hashlib
import json
import os
import shutil
import time
from dataclasses import asdict
from typing import Any

from colorama import Fore

from .structures import LintError, LintResult


def cache_config(
    crisp_cfg: dict[str, Any], ruff_cfg: dict[str, Any], black_cfg: dict[str, Any]
) -> None:
    full_cfg = {"crisp": crisp_cfg, "ruff": ruff_cfg, "black": black_cfg}
    cache_dir = os.path.join(os.getcwd(), ".crisp_cache")
    cached_config_path = os.path.join(cache_dir, "config.json")

    if os.path.exists(cached_config_path):
        with open(cached_config_path) as f:
            old_cfg = json.load(f)

        if full_cfg != old_cfg:
            shutil.rmtree(cache_dir)
            print(
                f"{Fore.LIGHTYELLOW_EX}Changes to configuration detected. "
                "The cache has been purged.\n"
            )

    if not os.path.exists(cached_config_path):
        os.makedirs(cache_dir, exist_ok=True)

        with open(cached_config_path, "w") as f:
            json.dump(full_cfg, f)


def get_path_hash(path: str) -> str:
    h = hashlib.sha1()
    h.update(path.encode())
    return h.hexdigest()


def get_cached_lint_result(sources_path: str) -> LintResult:
    h = get_path_hash(sources_path)
    cached_result_path = os.path.join(os.getcwd(), ".crisp_cache", h[0], h[1], h)

    if not os.path.exists(cached_result_path):
        os.makedirs(os.path.dirname(cached_result_path), exist_ok=True)

        return LintResult(sources_path, check_time=time.time(), errors=[], cached=False)

    with open(cached_result_path) as f:
        cached_result_dict = json.load(f)

    check_time = cached_result_dict["check_time"]

    if os.stat(sources_path).st_mtime > check_time:
        return LintResult(sources_path, check_time=time.time(), errors=[], cached=False)

    errors: list[LintError] = []
    for error_dict in cached_result_dict["errors"]:
        errors.append(LintError(**error_dict))

    cached_result = LintResult(
        path=sources_path,
        check_time=check_time,
        errors=errors,
        needs_black=cached_result_dict["needs_black"],
        known_unfixable=cached_result_dict["known_unfixable"],
        cached=True,
    )
    return cached_result


def cache_lint_result(lint_result: LintResult) -> str:
    h = get_path_hash(lint_result.path)
    cached_result_path = os.path.join(os.getcwd(), ".crisp_cache", h[0], h[1], h)

    if not lint_result.cached:
        errors_dicts = [asdict(error) for error in lint_result.errors]
        cached_result_dict = {
            "check_time": lint_result.check_time,
            "errors": errors_dicts,
            "needs_black": lint_result.needs_black,
            "known_unfixable": lint_result.known_unfixable,
        }

        with open(cached_result_path, "w") as f:
            json.dump(cached_result_dict, f)

    return cached_result_path
