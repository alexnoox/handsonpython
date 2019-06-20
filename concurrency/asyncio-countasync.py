import logging
import asyncio

logging.basicConfig(level=logging.INFO, format="[%(threadName)s] %(asctime)-15s %(message)s ")


g_my_var = 0


async def increment(seconds: int):
    while True:
        global g_my_var
        g_my_var += 1
        # await asyncio.sleep(seconds)


async def display(seconds: int):
    while True:
        global g_my_var
        logging.info(g_my_var)
        await asyncio.sleep(seconds)


async def main():
    await asyncio.gather(increment(10), display(1))


if __name__ == "__main__":
    import time
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    logging.info(f"{__file__} executed in {elapsed:0.2f} seconds.")
