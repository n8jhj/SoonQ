"""Utility functionalities.

Functions:
echo - Wrapper for click.echo.
get_taskclass - Get subclass of BaseTask by name.
"""

import functools
import inspect
import pathlib

import click

import soonq as sq


@functools.wraps(click.echo)
def echo(*args, **kwargs):
    """Wrapper for click.echo."""
    return click.echo(*args, **kwargs)


def get_taskclass(name):
    """Returns the named subclass of BaseTask. Raises a ValueError if
    the class name is not recognized.
    """
    # TODO: Remove this.  Importing here now to avoid circular import.
    import examples

    istasksubclass = lambda x: inspect.isclass(x) and issubclass(
        x, sq.BaseTask
    )
    task_classes = dict(inspect.getmembers(examples, istasksubclass))
    try:
        task_cls = task_classes[name]
    except KeyError:
        raise ValueError(f"Unrecognized task class name {name!r}")
    return task_cls
