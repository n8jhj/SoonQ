import sys

from . import (
    clear_queue, error_task, error_worker, timer_task, timer_worker,
    view_queue, view_work)
import soonq as sq


def execute(command):
    try:
        getattr(sys.modules[__name__], command)()
    except AttributeError:
        sq.echo(f"Example {command!r} not recognized.")


command = sys.argv[1]
execute(command)
