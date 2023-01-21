"""A callable script used elsewhere with the subprocess module for
running a single task.
"""

import sys

from .commands import run_work


try:
    task_class_name, task_id = sys.argv[1:]
except ValueError:
    raise RuntimeError(f"Necessary arguments not passed to {__file__}")

run_work(task_class_name, task_id)
