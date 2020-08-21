import sys

from . import \
    clear_queue, error_task, error_worker, task_items, timer_task, timer_worker
import soonq as sq


def execute(command):
    try:
        getattr(sys.modules[__name__], command)()
    except AttributeError:
        sq.echo(f"Example {command!r} not recognized.")


command = sys.argv[1]
execute(command)
