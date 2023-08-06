import asyncio


class AioVtyClient:
    def __init__(self, name: str):
        self.name = name
        self.prompt_char = '>'
        self.node = ''
        self.reader = None
        self.writer = None

    async def connect(self, host, port):
        self.reader, self.writer = await asyncio.open_connection(host, port)
        return await self.read()

    async def close(self):
        self.writer.close()
        await self.writer.wait_closed()

    async def enable(self):
        await self.write(b'enable')
        self.prompt_char = '#'
        await self.read()

    async def disable(self):
        await self.write(b'disable')
        self.prompt_char = '>'
        await self.read()

    async def command(self, command):
        await self.write(command)
        data = (await self.read())[len(command):].strip(b'\r\n')
        return data

    async def configure_terminal(self):
        await self.command(b'configure terminal')

    async def end(self):
        await self.command(b'end')

    async def read(self):
        # Read until a new line feed.
        node_indicator = b''
        data = b''
        while node_indicator not in (b'(', self.prompt_char.encode()):
            data += node_indicator
            data += (await self.reader.readuntil(self.name.encode()))[:-len(self.name.encode())]
            node_indicator = await self.reader.read(1)
        if node_indicator == self.prompt_char.encode():
            # Node mode exited.
            self.node = ''
            await self.reader.read(len(' '))
            return data
        # Update node.
        self.node = (await self.reader.readuntil(b')'))[:-len(b')')].decode()
        await self.reader.readuntil(f'{self.prompt_char} '.encode())
        return data

    async def write(self, line):
        self.writer.write(line + b'\n')
        await self.writer.drain()
