import asyncio
import time


async def say_after(delay, what):
    print(f"enter sleep_after, delay = {delay}, what = {what}")
    await asyncio.sleep(delay)
    print(f"exit sleep_after, delay = {delay}, what = {what}")


async def main():
    task1 = asyncio.create_task(
        say_after(1, 'task1'))

    task2 = asyncio.create_task(
        say_after(2, 'task2'))

    print(f"started at {time.strftime('%X')}")

    print("Start sync sleeping")
    time.sleep(1)
    print("Start async sleeping")
    await asyncio.sleep(2)
    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    print("awaiting task 1")
    await task1
    print("awaiting task 2")
    await task2
    print("finishing")

    print(f"finished at {time.strftime('%X')}")

asyncio.run(main())
