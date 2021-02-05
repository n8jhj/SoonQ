"""Utility functionalities.

Functions:
echo - Wrapper for click.echo.
"""

import functools

import click


@functools.wraps(click.echo)
def echo(*args, **kwargs):
    """Wrapper for click.echo."""
    return click.echo(*args, **kwargs)
