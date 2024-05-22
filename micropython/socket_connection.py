import asyncio
import json

def log(msg):
    print(msg)
    # pass

class SocketConnection():
    def __init__(self):
        self.connected = False
        self.reader = None
        self.writer = None
        self.purpose_handlers = {}
        self.connect_callbacks = []
        self.writer_lock = asyncio.Lock()

    async def handle_connection(self, reader, writer):
        if self.connected:
            # Only one connection is allowed
            print(f"Can only support one connection, closing new connection from {writer.get_extra_info('peername')!r}")
            reader.close()
            await reader.wait_closed()
            writer.close()
            await writer.wait_closed()
        else:
            print(f"Got connection from {writer.get_extra_info('peername')!r}")
            self.connected = True
            self.reader = reader
            self.writer = writer
            for callback in self.connect_callbacks:
                await callback()

    async def run_reader(self):
        while True:
            if self.connected:
                try:
                    socket_data = await self.reader.read(2)
                except OSError as e:
                    # The connection died for some reason
                    print("Connection died waiting for read")
                    self.connected = False
                    continue

                if len(socket_data) == 0:
                    print("Tried to read 2 bytes, got none. Connection probably dead")
                    self.connected = False
                    continue

                num_data_bytes = int.from_bytes(socket_data, "big")

                if num_data_bytes == 0:
                    print("No more bytes to read, waiting for more data")
                    continue

                try:
                    socket_data = await self.reader.read(num_data_bytes)
                except OSError as e:
                    # The connection died for some reason
                    print("Connection died waiting for read")
                    self.connected = False
                    continue

                num_bytes_recieved = len(socket_data)
                if num_bytes_recieved < num_data_bytes:
                    print(f"Tried to read {num_data_bytes} bytes, got {num_bytes_recieved}. Connection probably dead.")
                    self.connected = False
                    continue

                data = json.loads(socket_data.decode("ascii"))
                print(f"Recieved: {data}")

                if not isinstance(data, dict):
                    print(f"Recieved invalid datatype - needs to be a dict.")
                    continue

                if "purpose" not in data:
                    print(f"'purpose' key not in data.")
                    continue

                if "body" not in data:
                    print(f"'body' key not in data.")
                    continue   

                purpose = data["purpose"]
                if purpose in self.purpose_handlers:
                    self.purpose_handlers[purpose](data["body"])
                else:
                    print(f"No handler registered for {purpose} purpose.")
                    continue

            else:
                # Wait for the socket connection to come back online
                await asyncio.sleep(0.5)

    async def write(self, data):
        """
        Write data to the connected client.

        The caller should check to see if the socket is connected before
        sending, but extra checks are performed in this method as well.

        The socket could disconnect at any moment so this method is
        quite defensive.

        Args:
            data (<json serialisable object>): The data to send. This is
                typically a dictionary.
        """

        if not self.connected:
            return

        # There may be more than one task calling this method, bad
        # things will probably happen if two tasks try to write data
        # to the socket concurrently...
        async with self.writer_lock:
            to_send = bytearray(2)
            msg_bytes = bytes(json.dumps(data), "ascii")
            uint16_len_bytes = len(msg_bytes).to_bytes(2, "big")
            to_send.extend(msg_bytes)
            to_send[0] = uint16_len_bytes[0]
            to_send[1] = uint16_len_bytes[1]
            # One last check to see that we're still connected
            if self.connected:
                log(f"sending data (len {len(msg_bytes)}) {to_send}")
                self.writer.write(to_send)
                await self.writer.drain()