from collections import defaultdict

from pycodestyle import StandardReport, StyleGuide

from .config import Config
from .structures import LintError, LintResult


class CustomPycodestyleReport(StandardReport):
    def __init__(self, options) -> None:
        super().__init__(options)

        self.lint_errors: dict[str, list[LintError]] = defaultdict(list)

    def get_file_results(self) -> None:
        for line, col, code, msg, _doc in self._deferred_print:
            error = LintError(line, col, code, msg)
            self.lint_errors[self.filename].append(error)


def run_pycodestyle(results: list[LintResult]) -> None:
    guide = StyleGuide(
        max_line_length=Config().line_length,
        ignore=Config().pycodestyle_ignore,
        reporter=CustomPycodestyleReport,
    )
    report: CustomPycodestyleReport = guide.check_files([r.path for r in results])

    for r in results:
        r.errors.extend(report.lint_errors[r.path])
