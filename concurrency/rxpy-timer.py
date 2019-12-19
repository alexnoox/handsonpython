import concurrent.futures
import logging
import multiprocessing
import random
import time

import rx
from rx.scheduler import ThreadPoolScheduler
from rx import operators as ops

logging.basicConfig(level=logging.INFO, format="[%(threadName)s] %(asctime)-15s %(message)s ")

# calculate number of CPU's, then create a ThreadPoolScheduler with that number of threads
optimal_thread_count = multiprocessing.cpu_count()
pool_scheduler = ThreadPoolScheduler(optimal_thread_count)

def intense_calculation(value):
    # sleep for a random short duration between 0.5 to 2.0 seconds to simulate a long-running calculation
    time.sleep(random.randint(5, 20) * 0.1)
    return value

with concurrent.futures.ProcessPoolExecutor(5) as executor:
    rx.interval(1).pipe(
        ops.observe_on(pool_scheduler),
        ops.map(lambda i: i * 100),
        # ops.map(lambda s: intense_calculation(s))
        # ops.map(lambda s: executor.submit(intense_calculation, s))
    ).subscribe(
        on_next=lambda i: logging.info(f"interval: {i}"),
        on_error=lambda e: print(e)
    )

input("Press any key to exit\n")
