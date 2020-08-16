"""For viewing info about tasks in queue.
"""

import pprint

import soonq as sq


def task_items():
    sq.echo(pprint.pformat(list(sq.task_items(max_entries=5))))
