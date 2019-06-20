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
    time.sleep(random.randint(1, 10) * .1)
    return value

# calculate number of CPU's, then create a ThreadPoolScheduler with that number of threads
optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

global_ids = []

def set_ids(id) -> None:
    global global_ids
    global_ids.append(id)

def get_ids():
    global global_ids
    return global_ids

rx.interval(10).pipe(
    ops.map(lambda i: i * 100),
    ops.observe_on(pool_scheduler),
    ops.do_action(lambda _: set_ids(_)),
    ops.map(lambda s: intense_calculation(s))
).subscribe(
    on_next=lambda i: logging.info(f"PROCESS 10s: {i}"),
    on_error=lambda e: logging.error(e)
)

rx.interval(1).pipe(
    ops.map(lambda i: i * 100),
    ops.flat_map(get_ids()),
    ops.observe_on(pool_scheduler),
    ops.map(lambda s: intense_calculation(s))
).subscribe(
    on_next=lambda i: logging.info(f"PROCESS 1s: {i}"),
    on_error=lambda e: logging.error(e)
)

input("Press any key to exit\n")