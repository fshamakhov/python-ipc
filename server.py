import asyncio
import os
from asyncio import AbstractServer, StreamReader, StreamWriter


class ServiceExit(Exception):
    """
    Custom exception which is used to trigger the clean exit
    of all running threads and the main program.
    """
    pass


def handle_exception(loop, context):
    pass


async def shutdown(signal=None):
    print('performing shutdown')
    if signal:
        print(f'Received exit signal {signal.name}...')
    await asyncio.sleep(0.1)


async def handle_echo(reader: StreamReader, writer: StreamWriter):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")
    if message == 'terminate':
        writer.write('Terminating this process'.encode())
        await writer.drain()
        await shutdown()
        raise SystemExit('Terminating main thread with SystemExit')

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()


async def run(server: AbstractServer):
    while True:
        print(f'serving: {server.is_serving()}')
        await asyncio.sleep(1)


async def main():
    loop = asyncio.get_event_loop()
    loop.set_exception_handler(handle_exception)
    server: AbstractServer = await asyncio.start_server(
        handle_echo, port=os.getenv('SERVER_PORT'))

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')
    await run(server)


if __name__ == '__main__':
    try:
        asyncio.run(main(), debug=True)
    except (SystemExit, KeyboardInterrupt, ServiceExit):
        print('Terminating main thread')
        exit(0)
