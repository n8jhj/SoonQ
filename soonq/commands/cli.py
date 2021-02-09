"""Command line interface.
"""

import click

from .commands import (
    clear_queue,
    task_items,
    stop_all_workers,
)
from ..utils import get_taskclass
from ..worker import start_worker_process, Worker


@click.group()
def soonq():
    """SoonQ: Subprocess-based queueing."""
    pass


@soonq.command()
def clear():
    """Clear the queue."""
    clear_queue()


@soonq.command()
@click.option(
    "-a/-A",
    "--all-entries/--head-only",
    default=False,
    show_default=True,
    help="Whether to show all entries.",
)
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
@click.argument("queue_name")
@click.argument("args", nargs=-1)
def enqueue(queue_name, args):
    """Enqueue a single task in the named queue."""
    task_cls = get_taskclass(queue_name)
    inst = task_cls()
    inst.delay(*args)


@soonq.command()
@click.argument("queue_name")
def worker(queue_name):
    """Start a worker on the named queue in the current process."""
    task_cls = get_taskclass(queue_name)
    inst = task_cls()
    worker = Worker(inst)
    worker.start()


@soonq.command()
@click.argument("queue_name")
def run(queue_name):
    """Run a single task from the named queue."""
    start_worker_process(queue_name)


@soonq.command()
@click.argument("queue_name")
@click.option(
    "-t",
    "--terminate",
    is_flag=True,
    help="Whether to immediately terminate the currently running task.",
)
def stop(queue_name, terminate):
    """Stop all Workers on the named task."""
    stop_all_workers(queue_name, terminate)
