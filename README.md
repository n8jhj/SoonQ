# SoonQ
A subprocess-based task queue.

## Introduction
SoonQ implements a simple FIFO queue using SQLite. It was created primarily for running long simulations.

As of yet, the vision of a subprocess-based workflow has not been realized. However, the package still works as a task queue.

## Installation
`pip install soonq`

## Usage
Users must create their own subclass of `soonq.BaseTask`. Subclasses must define a `run()` method, which contains the business logic for the task (what we care about). At least for now, input arguments to this method are restricted to being JSON serializable.

## Example

The following can be found in the examples directory.

**timer_task.py:**

    """Script for creating timer tasks.
    """

    import time

    import soonq as sq


    def timer_sleep_all(interval, n):
        for i in range(n):
            timer_sleep(interval, i, n)


    def timer_sleep(interval, i=None, n=None):
        if None not in (i, n):
            msg = f"{i+1}/{n} "
        else:
            msg = ''
        msg += f"Sleeping {interval} seconds..."
        sq.echo(msg)
        time.sleep(interval)


    class TimerTask(sq.BaseTask):
        """Task to count to a certain number a specified number of times.
        """

        task_name = 'TimerTask'

        def run(self, interval, n):
            """Count at the given interval the given number of times.

            Positional arguments:
            interval - (int) Interval, in seconds.
            n - (int) Number of times to count the given interval.
            """
            self.interval = interval
            timer_sleep_all(interval, n)
            sq.echo(f'Slept {interval * n} seconds total.')


    if __name__ == '__main__':
        # Create a new task.
        timer_task = TimerTask()
        # Add the task to the queue, to be executed at some future time.
        # Arguments to delay() are the same as for run().
        timer_task.delay(3, 3)

**timer_worker.py**

    """Script for runnning a Worker dedicated to accomplishing TimerTasks.
    """

    import soonq as sq

    from timer_task import TimerTask


    if __name__ == "__main__":
        # Instantiate TimerTask.
        timer_task = TimerTask()

        # Run worker.
        worker = sq.Worker(task=timer_task)
        worker.start()

## Running the examples

Example files are included in the examples directory. From within your repository, clone SoonQ...

`git clone https://github.com/n8jhj/SoonQ.git`

...and then install it in editable mode. Be careful to include the dot!

`pip install -e .`

Now run the following in two separate terminals:

**Terminal 1:**

Run the same script a few times.

    C:\Users\...>python examples\timer_task.py
    Queued task: 913d56e9-a609-4b84-b937-479a94716527

    C:\Users\...>python examples\timer_task.py
    Queued task: da952424-98d9-42e1-8851-91a30924b94b

    C:\Users\...>python examples\timer_task.py
    Queued task: 7ec2887a-42a5-4cb6-a0f9-a30453d4c95c

    C:\Users\...>

**Terminal 2:**

    C:\Users\...>python examples\timer_worker.py
    Running task: 913d56e9-a609-4b84-b937-479a94716527
    1/3 Sleeping 3 seconds...
    2/3 Sleeping 3 seconds...
    3/3 Sleeping 3 seconds...
    Slept 9 seconds total.
    Finished task: 913d56e9-a609-4b84-b937-479a94716527

    Running task: da952424-98d9-42e1-8851-91a30924b94b
    1/3 Sleeping 3 seconds...
    2/3 Sleeping 3 seconds...
    3/3 Sleeping 3 seconds...
    Slept 9 seconds total.
    Finished task: da952424-98d9-42e1-8851-91a30924b94b

    Running task: 7ec2887a-42a5-4cb6-a0f9-a30453d4c95c
    1/3 Sleeping 3 seconds...
    2/3 Sleeping 3 seconds...
    3/3 Sleeping 3 seconds...
    Slept 9 seconds total.
    Finished task: 7ec2887a-42a5-4cb6-a0f9-a30453d4c95c

    Waiting for next task... (Ctrl + C to quit)

    Quitting

    C:\Users\...>

## Etymology
This project is named after my friend Soon-Kyoo, with whom I enjoyed countless bouts of epic ping-pong in college. People call him Q, for short.
