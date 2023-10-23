import asyncio
import random

# https://github.com/micropython/micropython-lib/blob/master/python-stdlib/functools/functools.py
def partial(func, *args, **kwargs):
    def _partial(*more_args, **more_kwargs):
        kw = kwargs.copy()
        kw.update(more_kwargs)
        return func(*(args + more_args), **kw)

    return _partial

async def create_jobs_forever(queue):
    while True:
        task_length = random.randint(1, 3) * 2
        print(f"Adding a job of {task_length} seconds")
        await queue.put(task_length)
        await asyncio.sleep(4)

async def consume_jobs_forever(queue):
    while True:
        item = await queue.get()
        print(f"Performing job of length {item} seconds.")
        await asyncio.sleep(item)
        partial_func = partial(dummy, "hello")
        await partial_func()
        queue.task_done()

async def check_queue_length_forever(queue):
    while True:
        print(f"--- There are {queue.qsize()} items in the queue")
        await asyncio.sleep(1)

async def dummy(msg):
    print(f"Dummy call: {msg}")


async def main():
    queue = asyncio.Queue()

    # # This didn't work - only tasks were created
    
    # # Start creating tasks
    # await create_jobs_forever(queue)
    
    # # Start consuming tasks
    # await consume_jobs_forever(queue)




    # # This didn't work - we never get past check_queue_length_forever
    # # because it never returns. It does sleep, so control is handed back
    # # to the main loop, but (further up the main loop?) we were never
    # # able to start other tasks.
    
    # # Start checking the length of the queue
    # await check_queue_length_forever(queue)
    
    # # Start consuming tasks
    # await consume_jobs_forever(queue)

    # # Start creating tasks
    # await create_jobs_forever(queue)




    # This only runs for 1 second
    # https://stackoverflow.com/questions/56377402/why-is-asyncio-queue-await-get-blocking
    # asyncio.create_task(check_queue_length_forever(queue))
    # asyncio.create_task(consume_jobs_forever(queue))
    # asyncio.create_task(create_jobs_forever(queue))
    # await asyncio.sleep(1)





    # # Run all tasks concurrently
    queue.put_nowait(7)
    queue.put_nowait(7)
    await asyncio.gather(
        create_jobs_forever(queue),
        consume_jobs_forever(queue),
        check_queue_length_forever(queue)
    )


if __name__ == "__main__":
    asyncio.run(main())