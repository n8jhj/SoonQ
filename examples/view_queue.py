"""For viewing info about tasks in the queue.
"""

import pprint

import soonq as sq


def view_queue():
    sq.echo(pprint.pformat(list(sq.task_items(max_entries=5))))
