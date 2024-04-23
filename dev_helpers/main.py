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

class Foo():

    def __init__(self):
        self.lock = asyncio.Lock()
        self.nums = []

    async def process(self, num):
        async with self.lock:
            for i in range(1, num + 1):
                print(f"foo{i}/{num}")
                await asyncio.sleep(0.5)

    async def add_to_list(self, num):
        # async with self.lock:
        self.nums.append(num)
        for i in range(1, 4):
            print(f"Just added {num}, nums is {self.nums} ({i}/3)")
            await asyncio.sleep(0.5)

async def process_a_foo(foo, num):
    while True:
        await foo.process(num)
        

async def add_to_a_foo(foo, num, sleep):
    while True:
        await foo.add_to_list(num)
        await asyncio.sleep(sleep)

async def main_lock():
    f = Foo()
    tasks = []
    # tasks.append(asyncio.create_task(process_a_foo(f, 3)))
    # tasks.append(asyncio.create_task(process_a_foo(f, 5)))
    tasks.append(asyncio.create_task(add_to_a_foo(f, 3, 2)))
    tasks.append(asyncio.create_task(add_to_a_foo(f, 5, 4)))
    await asyncio.gather(*tasks)


async def main_concurrent():
    delay_task = asyncio.create_task(forever_delayer())
    printer_task = asyncio.create_task(forever_printer())
    await delay_task
    await printer_task

async def main_sequential():
    while True:
        await delayer()
        await printer()

asyncio.run(main_lock())