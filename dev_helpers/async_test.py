import asyncio
import random

async def delayer():
    print("Beginning")
    delay = random.randint(1,5)
    print(f"Delaying {delay} seconds.")
    await asyncio.sleep(delay)
    print("Finished")

async def printer():
    for i in range(10):
        await asyncio.sleep(0.1)
        print(f"Printer {i}")

async def forever_delayer():
    while True:
        print("Beginning")
        delay = random.randint(1,5)
        print(f"Delaying {delay} seconds.")
        await asyncio.sleep(delay)
        print("Finished")

async def forever_printer():
    while True:
        for i in range(10):
            await asyncio.sleep(0.2)
            print(f"Printer {i}")



async def main_concurrent():
    delay_task = asyncio.create_task(forever_delayer())
    printer_task = asyncio.create_task(forever_printer())
    await delay_task
    await printer_task

async def main_sequential():
    while True:
        await delayer()
        await printer()

asyncio.run(main_concurrent())