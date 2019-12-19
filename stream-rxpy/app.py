import logging
import multiprocessing
import time
import traceback
from typing import List

import rx
from rx import operators as ops
from rx.core import typing
from rx.scheduler import ThreadPoolScheduler
from rx.subject import Subject

logging.basicConfig(level=logging.DEBUG, format="[%(threadName)s] %(asctime)-15s %(message)s ")


def print_error(message: str, e: Exception):
    logging.error(f"error: {message}: {e}")
    logging.error(f"error: {traceback.print_exc()}")


class ApiClient:
    def __init__(self):
        self.data: List[float] = []

    def fetch_subjects(self) -> List[float]:
        logging.debug(f"in fetch_subjects with {self.data}")
        time.sleep(1.5)  # simulate a call duration
        self.data.append(len(self.data))
        logging.debug(f"out fetch_subjects {len(self.data)}")
        return self.data


class MyObserver(typing.Observer[float]):
    def __init__(self):
        logging.debug("in MyObserver.__init__")
        super().__init__()

    def on_next(self, value: float) -> None:
        logging.debug(f"in MyObserver.on_next {value}")

    def on_error(self, error: Exception) -> None:
        print_error("Error in MyObserver", error)

    def on_completed(self) -> None:
        logging.debug("in MyObserver.on_completed")


class MySubject(typing.Subject[float, float]):
    def __init__(self):
        logging.debug("in MySubject.__init__")

        self.bfc = ApiClient()
        self.subject: typing.Subject[float, float] = Subject()

    def on_next(self, value: float) -> None:
        logging.debug(f"in MySubject.on_next {value}")
        self.subject.on_next(value)

    def on_error(self, error: Exception) -> None:
        print_error("Error in MySubject", error)

    def on_completed(self) -> None:
        logging.debug("in MySubject.on_completed")

    def subscribe(self, observer: typing.Observer[float] = None, *, scheduler: typing.Scheduler = None) -> typing.Disposable:
        logging.debug("in MySubject.subscribe")
        return self.subject.subscribe(observer)


class MyObservable(typing.Observable):
    def __init__(self, scheduler):
        logging.debug("in MyObservable.__init__")

        self.bfc = ApiClient()
        self.scheduler = scheduler
        self.subject: Subject[List[float], float] = Subject()

    def start(self):
        logging.debug("in MyObservable.start")
        rx.interval(1.0).pipe(
            ops.subscribe_on(self.scheduler),
            ops.flat_map(lambda i: self.fetch_subjects())
        ).subscribe(
            on_next=lambda v: self.subject.on_next(v),
            on_error=lambda e: print_error("Error in interval loop", e)
        )

    def fetch_subjects(self) -> List[float]:
        logging.debug("in MyObservable.fetch_subjects")
        return self.bfc.fetch_subjects()

    def subscribe(self, subject: typing.Subject[List[float], float] = None, *, scheduler: typing.Scheduler = None) -> typing.Disposable:
        logging.debug("in MyObservable.subscribe")
        return self.subject.subscribe(subject)


def main():
    logging.info("in main")

    optimal_thread_count = multiprocessing.cpu_count()
    thread_pool = ThreadPoolScheduler(optimal_thread_count)
    logging.info(f"using {optimal_thread_count} threads")

    observable = MyObservable(thread_pool)
    subject = MySubject()
    observer = MyObserver()

    observable.subscribe(subject)
    subject.subscribe(observer)

    observable.start()

    input('Press <enter> to quit\n')


if __name__ == '__main__':
    main()
