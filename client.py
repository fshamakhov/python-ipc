import asyncio
import os


async def tcp_echo_client(message):
    reader, writer = await asyncio.open_connection(
        os.getenv('SERVER_HOST'), os.getenv('SERVER_PORT'))

    print(f'Send: {message!r}')
    writer.write(message.encode())

    data = await reader.read(100)
    print(f'Received: {data.decode()!r}')

    await asyncio.sleep(1)

    print('Close the connection')
    writer.close()


if __name__ == '__main__':
    asyncio.run(tcp_echo_client('Hello World!'))
    asyncio.run(tcp_echo_client('terminate'))
