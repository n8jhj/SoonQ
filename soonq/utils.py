"""Utility functionalities.

Functions:
echo - Wrapper for click.echo.
tabulate_data - Tabulate data in a nice text table.
"""

import functools
import inspect
import pathlib

import click
from tabulate import tabulate

import soonq as sq
from .config import TABULATE_FORMATTING


@functools.wraps(click.echo)
def echo(*args, **kwargs):
    """Wrapper for click.echo."""
    return click.echo(*args, **kwargs)


def tabulate_data(data, headers=None):
    """Tabulate data in a nice text table."""
    return tabulate(data, headers=headers, **TABULATE_FORMATTING)
