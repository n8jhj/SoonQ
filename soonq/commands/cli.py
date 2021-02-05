"""Command line interface.
"""

import inspect

import click

import soonq as sq
from .commands import (
    clear_queue, task_items,
)
from ..worker import Worker
import examples


@click.group()
def soonq():
    """SoonQ: Subprocess-based queueing."""
    pass


@soonq.command()
def clear():
    """Clear the queue."""
    clear_queue()


@soonq.command()
@click.option('-a/-A', '--all-entries/--head-only', default=False,
    show_default=True,
    help="Whether to show all entries.")
def view(all_entries):
    """View tasks in the queue."""
    max_entries = None if all_entries else 5
    any_items = False
    for queue_item in task_items(max_entries=max_entries):
        any_items = True
        click.echo(queue_item)
    if not any_items:
        click.echo("Queue empty.")


@soonq.command()
@click.argument('queue_name')
@click.argument('args', nargs=-1)
def enqueue(queue_name, args):
    """Enqueue a single task in the named queue."""
    task_cls = get_taskclass(queue_name)
    inst = task_cls()
    inst.delay(*args)


@soonq.command()
@click.argument('queue_name')
def worker(queue_name):
    """Start a worker in the current process."""
    task_cls = get_taskclass(queue_name)
    inst = task_cls()
    worker = Worker(inst)
    worker.start()


@soonq.command()
@click.argument('queue_name')
def run(queue_name):
    """Run a single task from the named queue."""
    task_cls = get_taskclass(queue_name)
    inst = task_cls()
    worker = Worker(inst)
    worker.start()


def get_taskclass(name):
    """Returns the named subclass of BaseTask. Raises a ValueError if
    the class name is not recognized.
    """
    istasksubclass = (
        lambda x:
        inspect.isclass(x) and issubclass(x, sq.BaseTask)
    )
    task_classes = dict(inspect.getmembers(examples, istasksubclass))
    try:
        task_cls = task_classes[name]
    except KeyError:
        raise ValueError(f"Unrecognized task class name {name!r}")
    return task_cls
