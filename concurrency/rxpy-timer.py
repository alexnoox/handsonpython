import concurrent.futures
import time

import rx
from rx import operators as ops

seconds = [5, 1, 2, 4, 3]


def sleep(tm):
    time.sleep(tm)
    return tm


def output(result):
    print('%d seconds' % result)


rx.interval(1).pipe(
    ops.flat_map(lambda s: sleep(s))
).subscribe(output)
