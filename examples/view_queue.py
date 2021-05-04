"""View info about tasks in the queue.
"""

import soonq as sq
from soonq.commands import tabulate_task_items


def view_queue():
    sq.echo(tabulate_task_items(max_entries=5))
