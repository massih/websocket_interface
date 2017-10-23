#!/usr/bin/env python
import asyncio
import aioredis


async def init_redis():
    _redis = await aioredis.create_redis(('localhost', '6379'))
    await _redis.publish_json('websocket_interface', {'topic': 'topic', 'data': 'data11'})
    await _redis.publish_json('websocket_interface', {'topic': 'topic2', 'data': 'data21'})
    await _redis.publish_json('websocket_interface', {'topic': 'topic', 'data': 'data12'})
    await _redis.publish_json('websocket_interface', {'topic': 'topic2', 'data': 'data22'})


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_redis())
