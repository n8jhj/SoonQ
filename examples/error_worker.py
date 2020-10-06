"""Run a Worker dedicated to accomplishing ErrorTasks.
"""

import soonq as sq

from .error_task import ErrorTask


def error_worker():
    error_task = ErrorTask()
    worker = sq.Worker(task=error_task)
    worker.start()
