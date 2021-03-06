"""Create an ErrorTask which will cause an Exception.
"""

import random
import time

import soonq as sq


class ErrorTask(sq.BaseTask):
    """Task that results in an Exception."""

    def run(self):
        """Wait a random number of seconds before raising a
        RuntimeException.
        """
        sq.echo("Doing something rash...")
        time.sleep(random.choice([1, 2, 3]))
        raise RuntimeError("Rash choices produced a consequence.")


def error_task():
    error_task = ErrorTask()
    error_task.delay()
