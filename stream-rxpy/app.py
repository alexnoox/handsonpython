import logging
import multiprocessing
import time
import traceback

import rx
from rx import operators as ops
from rx.core import typing
from rx.core.typing import Scheduler, Disposable
from rx.scheduler import ThreadPoolScheduler

logging.basicConfig(level=logging.DEBUG, format="[%(threadName)s] %(asctime)-15s %(message)s ")


def print_error(message: str, e: Exception):
    logging.error(f"error: {message}: {e}")
    logging.error(f"error: {traceback.print_exc()}")


class ApiClient:
    def __init__(self):
        self.mcs = []

    def fetch_subjects(self):
        logging.debug(f"in fetch_subjects with {self.mcs}")
        time.sleep(1.5)  # simulate a call duration
        self.mcs.append(len(self.mcs))
        logging.debug(f"out fetch_subjects {len(self.mcs)}")
        return self.mcs


class MyObserver(typing.Observer):
    def __init__(self):
        logging.debug("in MyObserver.__init__")
        super().__init__()

    def on_next(self, value: int) -> None:
        logging.debug(f"in MyObserver.on_next {value}")

    def on_error(self, error: Exception) -> None:
        print_error("Error in MyObserver", error)

    def on_completed(self) -> None:
        logging.debug("in MyObserver.on_completed")


class MySubject(typing.Subject):
    def __init__(self):
        logging.debug("in MySubject.__init__")

        self.bfc = ApiClient()
        self.observers: list[MyObserver] = []

    def subscribe(self, observer: MyObserver = None, *, scheduler: Scheduler = None) -> Disposable:
        logging.debug("in MySubject.subscribe")
        self.observers.append(observer)

    def on_next(self, value: int) -> None:
        logging.debug(f"in MySubject.on_next {value}")
        rx.from_iterable(self.observers).subscribe(
            on_next=lambda o: o.on_next(value),
            on_error=lambda e: print_error("Error in MyObservable", e)
        )

    def on_error(self, error: Exception) -> None:
        print_error("Error in MySubject", error)

    def on_completed(self) -> None:
        logging.debug("in MySubject.on_completed")


class MyObservable(typing.Observable):
    def __init__(self):
        logging.debug("in MyObservable.__init__")

        self.bfc = ApiClient()
        self.observers: list[MySubject] = []

    def fetch_subjects(self):
        values = self.bfc.fetch_subjects()
        rx.from_iterable(self.observers).subscribe(
            on_next=lambda o: o.on_next(values),
            on_error=lambda e: print_error("Error in MyObservable", e)
        )

    def subscribe(self, observer: MySubject = None, *, scheduler: typing.Scheduler = None) -> typing.Disposable:
        logging.debug("in MyObservable.subscribe")
        self.observers.append(observer)


def main():
    logging.info("in main")

    optimal_thread_count = multiprocessing.cpu_count()
    thread_pool = ThreadPoolScheduler(optimal_thread_count)
    logging.info(f"using {optimal_thread_count} threads")

    observable = MyObservable()
    subject = MySubject()
    observer = MyObserver()

    observable.subscribe(subject)
    subject.subscribe(observer)

    rx.interval(1.0).pipe(
        ops.subscribe_on(thread_pool)
    ).subscribe(
        on_next=lambda i: observable.fetch_subjects(),
        on_error=lambda e: print_error("Error in interval loop", e)
    )

    input('Press <enter> to quit\n')


if __name__ == '__main__':
    main()
