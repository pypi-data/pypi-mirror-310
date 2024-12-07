from dataclasses import dataclass
from enum import Enum, IntEnum


@dataclass
class LintError:
    line: int
    col: int
    code: str
    msg: str


@dataclass
class LintResult:
    path: str
    check_time: float
    errors: list[LintError]
    cached: bool
    needs_black: bool = False
    known_unfixable: bool = False
    just_fixed: bool = False


class ReturnCode(IntEnum):
    no_error = 0
    lint_error = 1
    other_error = 2


class FileSelectionMode(Enum):
    default = 1
    modified = 2
    latest_commit = 3
    diff_main = 4
    all_files = 5


class ExcludePatternKind(Enum):
    exclude = 1
    include = 2
