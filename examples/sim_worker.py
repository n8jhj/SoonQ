"""For running a Worker dedicated to accomplishing SimTasks.
"""

import soonq as sq

from .sim_task import SimTask


def sim_worker():
    sim_task = SimTask()
    worker = sq.Worker(task=sim_task)
    worker.start()
