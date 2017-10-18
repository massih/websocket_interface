#!/usr/bin/env python
import asyncio
import json

import aioredis
import websockets


async def init_websocket():
    pass


async def init_redis():
    _redis = await aioredis.create_redis(('127.0.0.1', '6379'))


async def main():
    _redis = await init_redis()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.run_forever()
