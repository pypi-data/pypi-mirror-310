import asyncio
import time
from typing import Coroutine, Callable, Literal
from logging import getLogger

logger = getLogger(__name__)


class QueueItem:
    must_complete: bool

    def __init__(self, task_item: Callable | Coroutine, *args, **kwargs):
        self.task_item = task_item
        self.args = args
        self.kwargs = kwargs
        self.must_complete = False
        self.time = int(time.monotonic_ns())

    def __hash__(self):
        return id(self)

    def __lt__(self, other):
        return self.time < other.time

    async def run(self):
        try:
            if asyncio.iscoroutinefunction(self.task_item):
                await self.task_item(*self.args, **self.kwargs)
        except Exception as err:
            logger.error(
                f"Error {err} occurred in {self.task_item.__name__} with args {self.args} and kwargs" f" {self.kwargs}"
            )


class TaskQueue:
    """TaskQueue is a class that allows you to queue tasks and run them concurrently with a specified number of workers.

    Attributes:
        - `workers` (int): The number of workers to run concurrently. Default is 10.

        - `timeout` (int): The maximum time to wait for the queue to complete. Default is None. If timeout is provided
            the queue is joined using `asyncio.wait_for` with the timeout.

        - `queue` (asyncio.Queue): The queue to store the tasks. Default is `asyncio.PriorityQueue` with no size limit.

        - `on_exit` (Literal["cancel", "complete_priority"]): The action to take when the queue is stopped.

        - `mode` (Literal["finite", "infinite"]): The mode of the queue. If `finite` the queue will stop when all tasks
            are completed. If `infinite` the queue will continue to run until stopped.

        - `worker_timeout` (int): The time to wait for a task to be added to the queue before stopping the worker or
            adding a dummy sleep task to the queue.

        - `stop` (bool): A flag to stop the queue instance.

        - `tasks` (list): A list of the worker tasks running concurrently, including the main task that joins the queue.

        - `priority_tasks` (set): A set to store the QueueItems that must complete before the queue stops.
    """

    def __init__(
        self,
        size: int = 0,
        workers: int = 10,
        timeout: int = None,
        queue: asyncio.Queue = None,
        on_exit: Literal["cancel", "complete_priority"] = "complete_priority",
        mode: Literal["finite", "infinite"] = "infinite",
        worker_timeout: int = 60,
    ):
        self.queue = queue or asyncio.PriorityQueue(maxsize=size)
        self.workers = workers
        self.tasks = []
        self.priority_tasks = set()  # tasks that must complete
        self.timeout = timeout
        self.stop = False
        self.on_exit = on_exit
        self.mode = mode
        self.worker_timeout = worker_timeout

    def add(self, *, item: QueueItem, priority: int = 3, must_complete: bool = False):
        """Add a task to the queue.

        Args:
            item (QueueItem): The task to add to the queue.
            priority (int): The priority of the task. Default is 3.
            must_complete (bool): A flag to indicate if the task must complete before the queue stops. Default is False.
        """
        try:
            if self.stop:
                return
            item.must_complete = must_complete
            self.priority_tasks.add(item) if item.must_complete else ...
            if isinstance(self.queue, asyncio.PriorityQueue):
                item = (priority, item)
            self.queue.put_nowait(item)
        except asyncio.QueueFull:
            logger.error("Queue is full")

        except Exception as err:
            logger.error("%s: Error occurred in %s.add", err, self.__class__.__name__)

    async def worker(self):
        while True:
            try:
                if isinstance(self.queue, asyncio.PriorityQueue):
                    _, item = self.queue.get_nowait()

                else:
                    item = self.queue.get_nowait()

                if self.stop is False or item.must_complete:
                    await item.run()

                self.queue.task_done()
                self.priority_tasks.discard(item)

                if self.stop and (self.on_exit == "cancel" or len(self.priority_tasks) == 0):
                    self.cancel()
                    break

            except asyncio.QueueEmpty:
                if self.stop:
                    break

                if self.mode == "finite":
                    break

                sleep = QueueItem(asyncio.sleep, 1)
                self.add(item=sleep)
                await asyncio.sleep(self.worker_timeout)

            except Exception as err:
                logger.error("%s: Error occurred in %s worker", err, self.__class__.__name__)

    async def run(self, timeout: int = 0):
        start = time.perf_counter()
        try:
            self.tasks.extend(asyncio.create_task(self.worker()) for _ in range(self.workers))
            timeout = timeout or self.timeout
            queue_task = asyncio.create_task(self.queue.join())

            if timeout:
                main_task = asyncio.create_task(asyncio.wait_for(queue_task, timeout=timeout))
            else:
                main_task = queue_task
            self.tasks.append(main_task)
            await main_task

        except TimeoutError:
            logger.warning(
                "Timed out after %d seconds, %d tasks remaining", time.perf_counter() - start, self.queue.qsize()
            )
            self.stop = True

        except asyncio.CancelledError as _:
            logger.warning("Main task cancelled")

        except Exception as err:
            logger.warning("%s: An error occurred in %s.run", err, self.__class__.__name__)

        finally:
            await self.clean_up()

    def stop_queue(self):
        self.stop = True
        self.on_exit = "cancel"
        self.cancel()

    async def clean_up(self):
        try:
            if self.on_exit == "complete_priority" and len(self.priority_tasks) > 0:
                logger.warning(f"Completing {len(self.priority_tasks)} priority tasks...")
                queue_task = asyncio.create_task(self.queue.join())
                self.tasks.append(queue_task)
                await queue_task
            self.cancel()

        except asyncio.CancelledError as _:
            ...

        except Exception as err:
            logger.error("%s: Error occurred in %s.clean_up", err, self.__class__.__name__)

        finally:
            self.cancel()

    def cancel(self):
        for task in self.tasks:
            try:
                if not task.done():
                    task.cancel()
            except asyncio.CancelledError as _:
                ...
        self.tasks.clear()
