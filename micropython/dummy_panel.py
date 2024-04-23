import asyncio

class DummyPanel():
    """
    The user facing interface to the computer.
    """

    def __init__(self):
        self.display_ref = None

    async def set_head(self, value):
        await asyncio.sleep(0.1)
        await self.display_ref.set_head(value)

    async def set_data(self, value):
        await asyncio.sleep(0.1)
        await self.display_ref.set_data(value)