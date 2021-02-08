"""Implements worker classes.

Classes:
Worker
"""

import platform
from subprocess import Popen, CREATE_NEW_CONSOLE, PIPE

from .utils import echo


class Worker:
    """Basic worker class.

    Example Usage:
        task = AdderTask()
        worker = Worker(task=task)
        worker.start()
    """

    def __init__(self, task):
        self.task = task
        self.waiting = False

    def start(self):
        """Begin working on the assigned type of task."""
        while True:
            try:
                # Read database.
                dequeued_item = self.task.dequeue()
                if not dequeued_item:
                    if not self.waiting:
                        echo(f"Waiting for next task...\n")
                        self.waiting = True
                    continue
                self.waiting = False
                self.task.set_status("dequeued")
                task_id, _, _, _, task_args, task_kwargs = dequeued_item
                # Run.
                self.task.slate(task_args, task_kwargs)
                echo(f"Running task: {task_id}")
                # Pass off execution to subprocess.
                exc_info = self.subprocess_run(task_id)
                if exc_info:
                    echo(f"Error in task: {task_id}\n")
                    self.task.set_status("error")
                    self.task.record_exc(*exc_info)
                else:
                    echo(f"Finished task: {task_id}\n")
                    self.task.set_status("complete")
            except KeyboardInterrupt:
                self.quit()
                break

    def subprocess_run(self, task_id):
        popen_kwargs = dict(
            args=[
                "python",
                "soonq/commands/runtask.py",
                self.task.task_name,
                str(task_id),
            ],
        )
        if platform.system() == "Windows":
            popen_kwargs["creationflags"] = CREATE_NEW_CONSOLE
        else:
            # "If shell is True, it is recommended to pass args as a
            # string rather than as a sequence."
            # https://docs.python.org/3/library/subprocess.html#subprocess.Popen
            popen_kwargs["args"] = " ".join(popen_kwargs["args"])
            popen_kwargs["shell"] = True
        popen_kwargs["stdin"] = PIPE
        popen_kwargs["stderr"] = PIPE
        popen_kwargs["universal_newlines"] = True
        subp = Popen(**popen_kwargs)
        outs, errs = subp.communicate()
        return errs

    def quit(self):
        """Stop working."""
        echo("Quitting")
