# Use Python 3.6+

import multiprocessing
import random
import time

import rx
import rx.operators as ops
from rx.concurrency import ThreadPoolScheduler, ImmediateScheduler, CurrentThreadScheduler, VirtualTimeScheduler, TimeoutScheduler
import logging

logging.basicConfig(level=logging.INFO, format="[%(threadName)s] %(asctime)-15s %(message)s ")


def intense_calculation(value):
    # sleep for a random short duration between 0.5 to 2.0 seconds to simulate a long-running calculation
    time.sleep(random.randint(5, 20) * .1)
    return value

# calculate number of CPU's, then create a ThreadPoolScheduler with that number of threads
optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

# Create Process 1
rx.of("Alpha", "Beta", "Gamma", "Delta", "Epsilon").pipe(
    ops.map(lambda s: intense_calculation(s)),
    ops.subscribe_on(pool_scheduler)
).subscribe(
    on_next=lambda s: logging.info(f"PROCESS 1: {s}"),
    on_error=lambda e: logging.error(e),
    on_completed=lambda: logging.info("PROCESS 1 done!"),
    scheduler=pool_scheduler
)

# Create Process 2
rx.range(1, 10).pipe(
    ops.map(lambda s: intense_calculation(s)),
    ops.subscribe_on(pool_scheduler)
).subscribe(
    on_next=lambda i: logging.info(f"PROCESS 2: {i}"),
    on_error=lambda e: logging.error(e),
    on_completed=lambda: logging.info("PROCESS 2 done!")
)

# Create Process 3, which is infinite
rx.interval(1).pipe(
    ops.map(lambda i: i * 100),
    ops.observe_on(pool_scheduler),
    ops.map(lambda s: intense_calculation(s))
).subscribe(
    on_next=lambda i: logging.info(f"PROCESS 3: {i}"),
    on_error=lambda e: logging.error(e)
)

input("Press any key to exit\n")