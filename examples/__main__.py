"""Logic for when this module is called from the command line.
"""

import importlib
import sys

import soonq as sq

# Import example modules.
EXAMPLE_FUNCTIONS = (
    '.clear_queue', '.clear_work',
    '.error_task', '.error_worker',
    '.sim_task', '.sim_worker',
    '.timer_task', '.timer_worker',
    '.view_queue', '.view_work',
)
EXAMPLE_MODULES = [importlib.import_module(func, package='examples')
    for func in EXAMPLE_FUNCTIONS]
EXAMPLE_MODULE_MAP = {mod.__name__.rsplit('.', maxsplit=1)[-1]: mod
    for mod in EXAMPLE_MODULES}
EXAMPLE_MODULE_DESCRIPTIONS = [mod.__doc__.rstrip('\n')
    for mod in EXAMPLE_MODULES]


HELP_OPTIONS = ('-h', '--help')
OPTIONS = [(HELP_OPTIONS, "Show this message and exit.")]


def execute(command):
    try:
        cmd = getattr(EXAMPLE_MODULE_MAP[command], command)
    except AttributeError:
        sq.echo(f"Example {command!r} not recognized.")
        return
    cmd()


def print_help():
    sq.echo(f"Usage: python -m examples [OPTIONS] COMMAND [ARGS]...\n")
    sq.echo("Options:")
    for opts, desc in OPTIONS:
        sq.echo(f"  {', '.join(opts)}  {desc}")
    sq.echo()
    sq.echo("Commands:")
    max_modname_len = max(len(mod) for mod in EXAMPLE_MODULE_MAP)
    for cmd, descr in zip(
            EXAMPLE_MODULE_MAP.keys(), EXAMPLE_MODULE_DESCRIPTIONS):
        sq.echo(f"  {cmd:<{max_modname_len+2}}{descr}")


command = sys.argv[1]
if command in HELP_OPTIONS:
    print_help()
else:
    execute(command)
