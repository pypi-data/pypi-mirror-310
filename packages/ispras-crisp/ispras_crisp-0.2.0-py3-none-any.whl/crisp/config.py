import os
from copy import deepcopy
from typing import Any

import tomlkit
from colorama import Fore, Style
from deepmerge import Merger
from tomlkit.exceptions import TOMLKitError
from wcmatch import glob

from .cache import cache_config
from .exceptions import CrispError

DEFAULT_LINE_LENGTH = 88
DEFAULT_MAIN_BRANCH = "main"
DEFAULT_SELECT_RUFF = [
    "A",
    "ARG",
    "B",
    "C4",
    "COM",
    "D",
    "F",
    "I",
    "INP",
    "ISC",
    "N",
    "NPY",
    "Q",
    "RUF013",
    "UP",
]
DEFAULT_IGNORE_RUFF = [
    "B028",
    "B905",
    "COM812",
    "D10",
    "D203",
    "D212",
    "D213",
    "D214",
    "D215",
    "D401",
    "D404",
    "D405",
    "D406",
    "D407",
    "D408",
    "D409",
    "D410",
    "D411",
    "D412",
    "D413",
    "D414",
    "D415",
    "D416",
    "D417",
    "N803",
    "N806",
    "N812",
    "NPY002",
    "UP030",
    "UP032",
]
DEFAULT_IGNORE_PYCODESTYLE = ["E133", "E203", "E241", "E74", "W503", "W505"]


class SafeDict:
    def __init__(self, dict_: dict, prefix: str = "") -> None:
        self.dict = dict_
        self.prefix = prefix

    def get(self, key: str, type_: type = dict) -> Any:
        new_prefix = key if self.prefix == "" else f"{self.prefix}.{key}"

        value = self.dict.get(key)
        if value is None:
            return SafeDict({}, new_prefix) if type_ is dict else None

        if type_ is int:
            try:
                value = int(value)
            except (TypeError, ValueError) as err:
                msg = (
                    f"{Fore.LIGHTYELLOW_EX}{new_prefix}{Style.RESET_ALL} field has "
                    f"invalid type '{value.__class__.__name__}' (expected 'int')."
                )
                raise CrispError(msg) from err
        elif not isinstance(value, type_):
            msg = (
                f"{Fore.LIGHTYELLOW_EX}{new_prefix}{Style.RESET_ALL} field has invalid "
                f"type '{value.__class__.__name__}' (expected '{type_.__name__}')."
            )
            raise CrispError(msg)

        return SafeDict(value, new_prefix) if type_ is dict else value


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            raise RuntimeError("Config not initialized. Run 'Config.init()'.")

        return cls._instance

    @classmethod
    def init(cls, pyproject_toml_path: str, no_update: bool = False):
        if cls._instance is not None:
            raise RuntimeError("Config already initialized.")

        cls._instance = super().__new__(cls)
        cls._instance._load_pyproject_toml(pyproject_toml_path, no_update)

        return cls._instance

    def _load_pyproject_toml(self, path: str, no_update: bool = False) -> None:
        if not os.path.isfile(path):
            if no_update:
                raise CrispError(
                    "Could not find "
                    f"{Fore.LIGHTYELLOW_EX}pyproject.toml{Style.RESET_ALL} "
                    "and creating one is prohibited."
                )

            print(
                f"{Fore.LIGHTYELLOW_EX}Warning: pyproject.toml not found, "
                "creating one. Please add it to your Git repo."
            )
            pyproject = {}
        else:
            with open(path) as f:
                try:
                    pyproject = tomlkit.load(f)
                except TOMLKitError as err:
                    raise CrispError(
                        f"{Fore.LIGHTYELLOW_EX}{path}{Style.RESET_ALL} "
                        "is not a valid TOML."
                    ) from err

        tool_section: SafeDict = SafeDict(pyproject).get("tool")
        crisp_cfg = tool_section.get("crisp")
        ruff_lint_cfg = tool_section.get("ruff").get("lint").dict

        self.exclude = crisp_cfg.get("exclude", list) or []
        self.line_length = crisp_cfg.get("line-length", int) or DEFAULT_LINE_LENGTH
        self.default_branch = (
            crisp_cfg.get("default-branch", str) or DEFAULT_MAIN_BRANCH
        )
        self.pycodestyle_ignore = (
            crisp_cfg.get("pycodestyle-ignore", list) or DEFAULT_IGNORE_PYCODESTYLE
        )

        black_regex = "|".join(
            glob.translate(pattern, flags=glob.GLOBSTAR)[0][0][1:-1]
            for pattern in self.exclude
        )
        pyproject_overwrite = {
            "tool": {
                "crisp": {
                    "exclude": self.exclude,
                    "line-length": self.line_length,
                    "default-branch": self.default_branch,
                    "pycodestyle-ignore": self.pycodestyle_ignore,
                },
                "black": {
                    "extend-exclude": black_regex,
                    "line-length": self.line_length,
                },
                "ruff": {
                    "extend-exclude": self.exclude,
                    "line-length": self.line_length,
                },
            }
        }
        if not ruff_lint_cfg:
            ruff_select = tomlkit.array().multiline(True)
            ruff_select.extend(DEFAULT_SELECT_RUFF)
            ruff_ignore = tomlkit.array().multiline(True)
            ruff_ignore.extend(DEFAULT_IGNORE_RUFF)

            pyproject_overwrite["tool"]["ruff"].update(
                {"lint": {"select": ruff_select, "ignore": ruff_ignore}}
            )

        pyproject_before_merge = deepcopy(pyproject)
        Merger([(dict, ["merge"])], ["override"], ["override"]).merge(
            pyproject, pyproject_overwrite
        )
        config_changed = pyproject_before_merge != pyproject

        if config_changed:
            if no_update:
                raise CrispError(
                    "Crisp configuration in "
                    f"{Fore.LIGHTYELLOW_EX}pyproject.toml{Style.RESET_ALL} "
                    "is inconsistent. "
                    f"Run {Fore.LIGHTYELLOW_EX}crisp init{Style.RESET_ALL}."
                )
            else:
                with open(path, "w") as f:
                    tomlkit.dump(pyproject, f)

        cache_config(
            pyproject["tool"]["crisp"],
            pyproject["tool"]["ruff"],
            pyproject["tool"]["black"],
        )
