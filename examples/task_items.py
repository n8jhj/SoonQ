"""Script for viewing info about tasks in queue.
"""

import pprint

import soonq as sq


if __name__ == '__main__':
    sq.echo(pprint.pformat(list(sq.task_items(max_entries=5))))
