import logging
import multiprocessing
import random
import threading
import time
import traceback

import numpy as np
import rx
from rx import operators as ops
from rx.scheduler import ThreadPoolScheduler
from rx.subject import Subject

logging.basicConfig(level=logging.INFO, format="[%(threadName)s] %(asctime)-15s %(message)s ")

def print_error(message, e):
    logging.error(f"error: {message}: {e}")
    logging.error(f"error: {traceback.print_exc()}")

class CalcService:
    def __init__(self):
        self.values = [random.random()]
        logging.info(f"in CalcService.__init__ {self.values}")

    def get_values_loop(self):
        while True:
            x = self.values[:1]
            x.append(random.random())
            time.sleep(1)
            self.values = x
            logging.info(f"out CalcService.get_values_loop {self.values}")
            time.sleep(10)

    def fetch_values(self):
        # sleep for a random short duration between 2.0 to 3.0 seconds
        time.sleep(random.randint(20, 30) * .1)
        x = self.values
        logging.info(f"out CalcService.fetch_values {x}")
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

calc = CalcService()

x = threading.Thread(target=calc.get_values_loop, daemon=True)
x.start()

rx.interval(1.0).pipe(
    ops.observe_on(pool_scheduler),
    ops.flat_map(lambda _: calc.fetch_values()),
    ops.map(expand_array),
    ops.do_action(stream.on_next)
).subscribe(
    on_next=lambda data: logging.info(f"interval {data}"),
    on_error=print_error
)

input("Press any key to exit\n")
