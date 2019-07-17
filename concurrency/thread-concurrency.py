
import logging
import threading
import time

logging.basicConfig(level=logging.INFO, format="[%(threadName)s] %(asctime)-15s %(message)s ")


class FakeClient:
    def __init__(self):
        self.market_catalogues = []

    def fetch_market_catalogues(self):
        while True:
            logging.info(f"starting update_market_catalogues with {self.market_catalogues}")
            local_copy = self.market_catalogues
            local_copy.append(len(local_copy))
            time.sleep(1)
            self.market_catalogues = local_copy
            logging.info(f"finishing update_market_catalogues with {self.market_catalogues}")

            time.sleep(5)

    def fetch_market_books(self):
        logging.info(f"starting fetch_market_books with {self.market_catalogues}")
        time.sleep(1)
        logging.info(f"finishing fetch_market_books {len(self.market_catalogues)}")



if __name__ == "__main__":
    client = FakeClient()

    x = threading.Thread(target=client.fetch_market_catalogues, daemon=True)
    x.start()

    while True:
        client.fetch_market_books()
