import os

from psutil import Process


def is_pre_commit() -> bool:
    return Process(os.getppid()).name == "pre-commit"
