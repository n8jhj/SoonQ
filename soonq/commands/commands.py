"""Useful commands.

Classes:
QueueItem
WorkItem

Functions:
clear_queue - Clear the queue.
clear_work - Clear the table of work.
task_items - Info about items in the queue.
work_items - Info about items in the table of work.
run_work - Run a given BaseTask instance.
"""

import pickle
import sqlite3
import sys
import traceback

from soonq.config import DB_PATH, QUEUE_TABLENAME, WORK_TABLENAME
from soonq.utils import echo, get_taskclass


# TODO: Dynamically create QueueItem and WorkItem classes based on
# configured database column names.
# This will also involve updating __repr__ to dynamically reference the
# signature of __init__.


class QueueItem:
    def __init__(self, task_id, queue_name, position, published, args, kwargs):
        self.task_id = task_id
        self.queue_name = queue_name
        self.position = position
        self.published = published
        self.args = pickle.loads(args)
        self.kwargs = pickle.loads(kwargs)

    @classmethod
    def from_tuple(cls, tuple_):
        return cls(*tuple_)

    def __repr__(self):
        return "QueueItem({}={}, {}={}, {}={}, {}={}, {}={}, {}={})".format(
            "task_id",
            self.task_id,
            "queue_name",
            self.queue_name,
            "position",
            self.position,
            "published",
            self.published,
            "args",
            self.args,
            "kwargs",
            self.kwargs,
        )


class WorkItem:
    def __init__(
        self,
        task_id,
        queue_name,
        started,
        status,
        exc_type,
        exc_value,
        exc_traceback,
    ):
        self.task_id = task_id
        self.queue_name = queue_name
        self.started = started
        self.status = status
        self.exc_type = pickle.loads(exc_type)
        self.exc_value = pickle.loads(exc_value)
        self.exc_traceback = "".join(pickle.loads(exc_traceback).format())

    @classmethod
    def from_tuple(cls, tuple_):
        return cls(*tuple_)

    def __repr__(self):
        return (
            "WorkItem({}={}, {}={}, {}={}, {}={}, {}={}, {}={}, {}={})".format(
                "task_id",
                self.task_id,
                "queue_name",
                self.queue_name,
                "started",
                self.started,
                "status",
                self.status,
                "exc_type",
                self.exc_type,
                "exc_value",
                self.exc_value,
                "exc_traceback",
                "...",
            )
        )


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


def clear_work():
    """Clear the table of work."""
    con = sqlite3.connect(str(DB_PATH))
    with con:
        con.execute(
            f"""
            DELETE FROM {WORK_TABLENAME}
            """
        )
    con.close()
    echo("Cleared table of work.")


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
        items = map(QueueItem.from_tuple, c.fetchmany(size=max_entries))
    else:
        items = map(QueueItem.from_tuple, c.fetchall())
    con.close()
    return items


def work_items(max_entries=None):
    """Information about the items in the work queue. Returns a
    generator of WorkItems.

    Keyword arguments:
    max_entries - (int) (Default: None) Maximum number of items to
        return. Default is to return all entries.
    """
    con = sqlite3.connect(str(DB_PATH))
    with con:
        c = con.execute(
            f"""
            SELECT
                task_id,
                queue_name,
                started,
                status,
                args,
                kwargs,
                exc_type,
                exc_value,
                exc_traceback
            FROM {WORK_TABLENAME}
            ORDER BY started ASC
            """
        )
    if max_entries:
        items = map(WorkItem.from_tuple, c.fetchmany(size=max_entries))
    else:
        items = map(WorkItem.from_tuple, c.fetchall())
    con.close()
    return items

def remove_work(self, item):
    """Remove the given item from the work table."""
    con = sqlite3.connect(str(DB_PATH))
    with con:
        con.execute(
            f"""
            DELETE FROM {WORK_TABLENAME}
            WHERE task_id = ?
            """,
            (item.task_id,),
        )
    con.close()


def run_work(task_clsname, task_id):
    """Run the task in the work table with the given ID."""
    # Get task from work table.
    con = sqlite3.connect(str(DB_PATH))
    with con:
        c = con.execute(
            f"""
            SELECT
                task_id,
                queue_name,
                started,
                status,
                args,
                kwargs,
                exc_type,
                exc_value,
                exc_traceback
            FROM {WORK_TABLENAME}
            WHERE task_id = ?
            """,
            (task_id,),
        )
        (
            task_id,
            queue_name,
            started,
            status,
            task_args,
            task_kwargs,
            exc_type,
            exc_value,
            exc_traceback,
        ) = c.fetchone()
        # _, _, _, _, task_args, task_kwargs, _, _, _ = c.fetchone()
    con.close()
    # Run task.
    task_args = pickle.loads(task_args)
    task_kwargs = pickle.loads(task_kwargs)
    exc_info = None
    task = get_taskclass(task_clsname)()
    try:
        task.run(*task_args, **task_kwargs)
    except:
        # Any Exceptions will be saved.
        exc_info = list(sys.exc_info())
        exc_info[-1] = traceback.extract_tb(exc_info[-1])
    return exc_info
