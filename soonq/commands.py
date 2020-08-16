"""Useful commands.

Classes:
QueueInfo

Functions:
clear_queue - Clear the queue.
task_items - Info about items in the queue.
"""

from collections import namedtuple
import sqlite3

from .config import DB_PATH, QUEUE_TABLENAME, SCHEMA
from .utils import echo


QueueItem = namedtuple('QueueItem', SCHEMA[QUEUE_TABLENAME].keys())


def clear_queue():
    """Clear the task queue."""
    con = sqlite3.connect(str(DB_PATH))
    with con:
        con.execute(
            f"""
            DELETE FROM {QUEUE_TABLENAME}
            """
        )
    con.close()
    echo("Cleared the queue.")


def task_items(max_entries=None):
    """Information about the items in the task queue. Returns a
    generator of QueueItems.

    Keyword arguments:
    max_entries - (int) (Default: None) Maximum number of items to
        return. Default is to return all entries.
    """
    con = sqlite3.connect(str(DB_PATH))
    with con:
        c = con.execute(
            f"""
            SELECT task_id, queue_name, position, published, args, kwargs
            FROM {QUEUE_TABLENAME}
            ORDER BY position DESC
            """
        )
    if max_entries:
        items = map(QueueItem._make, c.fetchmany(size=max_entries))
    else:
        items = map(QueueItem._make, c.fetchall())
    con.close()
    return items
