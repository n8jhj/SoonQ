"""Create a SimTask which will run a short simulation.
"""

import random
import string
import time

import soonq as sq


class Project:
    def __init__(self, name):
        self.name = name

    def run(self):
        n = 4
        for i in range(n):
            msg = f"{i+1}/{n} Simulation step"
            sq.echo(msg)
            time.sleep(2)


class SimTask(sq.BaseTask):
    """Task to perform an arbitrary simulation.
    """

    task_name = 'SimTask'

    def run(self, project):
        """Simulate subject to the parameters specified in the given
        project.
        """
        sq.echo(f"Running {project.name!r}...")
        project.run()
        sq.echo(f"Project {project.name!r} finished.")


def sim_task():
    # Create new Project.
    letter = random.choice(string.ascii_uppercase)
    project = Project(f"Project {letter}")
    # Create new SimTask and add it to the queue with the Project.
    sim_task = SimTask()
    sim_task.delay(project)
