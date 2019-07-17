import logging
import multiprocessing
import random
import time

import numpy as np

import rx
from rx.subjects import Subject
from rx.concurrency import ThreadPoolScheduler
from rx import operators as ops

logging.basicConfig(level=logging.INFO, format="[%(threadName)s] %(asctime)-15s %(message)s ")


def intense_calculation():
    # sleep for a random short duration between 2.0 to 4.0 seconds
    time.sleep(random.randint(20, 40) * .1)
    x = np.random.randn(3, 4)
    logging.info(f"out intense_calculation {x}")
    return x

def expand_array(values):
    logging.info(f"in expand_array values {values}")
    rows = list()
    for v in values:
        rows.append([v - 1, v, v + 1])
    logging.info(f"out expand_array rows {rows}")
    return rows

optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

stream = Subject()

stream.pipe(
    ops.observe_on(pool_scheduler),
    ops.do_action(lambda rows: logging.info(f"default {rows}"))
).subscribe()

# Flatmapper
stream.pipe(
    ops.do_action(lambda row: logging.info(f"flat_map {row}")),
    ops.flat_map(lambda x: x),
    ops.observe_on(pool_scheduler),
    ops.do_action(lambda row: logging.info(f"flat_map {row}"))
).subscribe()

while True:
    rx.from_(intense_calculation()).pipe(
        ops.flat_map(expand_array),
        ops.do_action(stream.on_next)
    ).subscribe()
