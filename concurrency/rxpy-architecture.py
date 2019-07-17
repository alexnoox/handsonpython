import logging
import multiprocessing
import random
import time
import traceback

import numpy as np

import rx
from rx.subjects import Subject
from rx.concurrency import ThreadPoolScheduler
from rx import operators as ops

logging.basicConfig(level=logging.INFO, format="[%(threadName)s] %(asctime)-15s %(message)s ")

def print_error(message, e):
    logging.error(f"error: {message}: {e}")
    logging.error(f"error: {traceback.print_exc()}")

def intense_calculation():
    # sleep for a random short duration between 2.0 to 4.0 seconds
    time.sleep(random.randint(20, 40) * .1)
    # x = np.random.randn(3, 4)
    x = [random.random(), random.random(), random.random()]
    logging.info(f"out intense_calculation {x}")
    return x

def expand_array(value):
    logging.info(f"in expand_array values {value}")
    rows = [value - 1, value, value + 1]
    logging.info(f"out expand_array rows {rows}")
    return rows

optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

stream = Subject()

stream.pipe(
    ops.observe_on(pool_scheduler),
    ops.do_action(lambda rows: logging.info(f"default {rows}"))
).subscribe(on_error=print_error)

# Flatmapper
stream.pipe(
    ops.observe_on(pool_scheduler),
    ops.flat_map(lambda x: x),
    ops.do_action(lambda row: logging.info(f"flat_map {row}"))
).subscribe(on_error=print_error)

rx.interval(1.0).pipe(
    ops.observe_on(pool_scheduler),
    ops.flat_map(lambda _: intense_calculation()),
    ops.map(expand_array),
    ops.do_action(stream.on_next)
).subscribe(
    on_next=lambda data: logging.info(f"interval {data}"),
    on_error=print_error
)

input("Press any key to exit\n")
