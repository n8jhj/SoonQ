"""Command line interface.
"""

import click

from .commands import (
    clear_queue, task_items,
)


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
