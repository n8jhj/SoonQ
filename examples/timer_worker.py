"""For runnning a Worker dedicated to accomplishing TimerTasks.
"""

import soonq as sq

from .timer_task import TimerTask


def timer_worker():
    # Instantiate TimerTask.
    timer_task = TimerTask()
    # Run worker.
    worker = sq.Worker(task=timer_task)
    worker.start()
