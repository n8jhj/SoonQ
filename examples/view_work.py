"""For viewing items in the work table.
"""

import pprint

import soonq as sq


def view_work():
    sq.echo(pprint.pformat(list(sq.work_items(max_entries=5))))