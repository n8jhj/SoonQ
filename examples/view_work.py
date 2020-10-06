"""View items in the table of work.
"""

import pprint

import soonq as sq


def view_work():
    sq.echo(pprint.pformat(list(sq.work_items(max_entries=5))))
