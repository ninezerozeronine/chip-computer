import asyncio
import random
from queue import Queue

def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)

    return _partial

async def create_jobs_forever(queue):
    while True:
        num = random.randint(0, 10)
        task = partial(print, str(num))
        print(f"making task {num}")
        await queue.put(task)
        await asyncio.sleep(1)

async def consume_jobs_forever(queue):
    while True:
        job = await queue.get()
        job()
        await asyncio.sleep(2)
        queue.task_done()

async def test():
    await asyncio.sleep(1)
    print("hello")
    await asyncio.sleep(1)
    print("world")
    job_queue = Queue()
    await asyncio.gather(
        create_jobs_forever(job_queue),
        consume_jobs_forever(job_queue)
    )
def main():
    asyncio.run(test())
