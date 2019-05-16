import multiprocessing
import random
import time

from rx import of, range, interval
import rx.operators as ops
from rx.concurrency import ThreadPoolScheduler, ImmediateScheduler, CurrentThreadScheduler, VirtualTimeScheduler, TimeoutScheduler
import logging

logging.basicConfig(level=logging.INFO, format="[%(threadName)s] %(asctime)-15s %(message)s ")


def intense_calculation(value):
    # sleep for a random short duration between 0.5 to 2.0 seconds to simulate a long-running calculation
    time.sleep(random.randint(5, 20) * .1)
    return value


if __name__ == "__main__":
    # calculate number of CPU's, then create a ThreadPoolScheduler with that number of threads
    optimal_thread_count = multiprocessing.cpu_count()
    pool_scheduler = ThreadPoolScheduler(optimal_thread_count)
    imm_scheduler = ImmediateScheduler()
    ct_scheduler = CurrentThreadScheduler()
    to_scheduler = TimeoutScheduler()

    # Create Process 1
    of("Alpha", "Beta", "Gamma", "Delta", "Epsilon").pipe(
        ops.map(lambda s: intense_calculation(s))
    ).subscribe_(
        on_next=lambda s: logging.info(f"PROCESS 1: {s}"),
        on_error=lambda e: logging.error(e),
        on_completed=lambda: logging.info("PROCESS 1 done!"),
        scheduler=pool_scheduler
    )

    # Create Process 2
    range(1, 10).pipe(
        ops.map(lambda s: intense_calculation(s))
    ).subscribe_(
        on_next=lambda i: logging.info(f"PROCESS 2: {i}"),
        on_error=lambda e: logging.error(e),
        on_completed=lambda: logging.info("PROCESS 2 done!"),
        scheduler=pool_scheduler
    )

    # Create Process 3, which is infinite
    interval(1000).pipe(
        ops.map(lambda i: i * 100),
        ops.map(lambda s: intense_calculation(s))
    ).subscribe_(
        on_next=lambda i: logging.info(f"PROCESS 3: {i}"),
        on_error=lambda e: logging.error(e),
        scheduler=pool_scheduler
    )
