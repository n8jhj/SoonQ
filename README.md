# SoonQ

A subprocess-based task queue.

## Introduction

SoonQ implements a simple first-in-first-out (FIFO) queue using SQLite. It was created primarily to give a user direct control over running long simulations.

## Installation

`pip install soonq`

## Usage

Users must create their own subclass of `soonq.BaseTask`. Subclasses must define a `run()` method, which contains the business logic for the task (what we care about). Input arguments to this method are restricted to being serializable via the [pickle module](https://docs.python.org/3/library/pickle.html).

## Running the examples

Example files are included in the examples directory. Clone SoonQ in your desired location.

`C:\desired\location>git clone https://github.com/n8jhj/SoonQ.git`

Optionally create a virtual environment within this directory. Then navigate into the `SoonQ` directory and install it, being careful to include the dot.

`pip install .`

Now run the same command a couple times in a terminal to enqueue two `TimerTask`s (the source code is in the examples directory):

    C:\...\SoonQ>soonq enq TimerTask 3 3
    Queued task: 913d56e9-a609-4b84-b937-479a94716527

    C:\...\SoonQ>soonq enq TimerTask 3 3
    Queued task: da952424-98d9-42e1-8851-91a30924b94b

    C:\...\SoonQ>

You'll be able to see the tasks in the queue.

    C:\...\SoonQ>soonq view
    +-----------+------------+----------+---------------------+--------+--------+
    |  task_id  | queue_name | position |      published      |  args  | kwargs |
    +-----------+------------+----------+---------------------+--------+--------+
    | da952424- | TimerTask  |    1     | 2021-05-04 14:45:51 | (3, 3) |   {}   |
    | 913d56e9- | TimerTask  |    0     | 2021-05-04 14:45:50 | (3, 3) |   {}   |
    +-----------+------------+----------+---------------------+--------+--------+

Now begin a worker process.

    C:\...\SoonQ>soonq run TimerTask

A separate terminal will spawn to run the worker. In turn, the worker terminal will spawn task terminals as it works. So there are three levels of processes:

1. The **master** process. Controls workers.
2. The **worker** process. Runs a single worker. Can spawn tasks.
3. The **task** process. Runs a single task.

In the task terminal you will see the runtime text:

    1/3 Sleeping 3 seconds...
    2/3 Sleeping 3 seconds...
    3/3 Sleeping 3 seconds...
    Slept 9 seconds total.

Meanwhile, the worker terminal will show:

    Running task: 913d56e9-a609-4b84-b937-479a94716527
    Finished task: 913d56e9-a609-4b84-b937-479a94716527

    Running task: da952424-98d9-42e1-8851-91a30924b94b
    Finished task: da952424-98d9-42e1-8851-91a30924b94b

With the worker running, more tasks can be enqueued and will be processed as the worker gets to them. You can spawn more workers if you want. Enqueue more `TimerTask`s and try it out!

To stop all workers working on a certain queue at any time:

    C:\...\SoonQ>soonq stop TimerTask

This will have each worker finish its current task and then shut down. If the `--terminate` or `-t` option is used, the workers will stop working and shut down immediately.

## Etymology

This project is named after my friend Soon-Kyoo, with whom I enjoyed countless bouts of epic ping-pong in college. He goes by "Q".
