import asyncio

from outcome import Outcome

class DummyPanel():
    """
    The user facing interface to the computer.
    """

    def __init__(self):
        self.display_ref = None

    def set_display_ref(self, display):
        self.display_ref = display

    async def set_head(self, value):
        await asyncio.sleep(0.1)
        await self.display_ref.set_head(value)
        return Outcome(True)

    async def set_data(self, value):
        await asyncio.sleep(0.1)
        await self.display_ref.set_data(value)
        return Outcome(True)