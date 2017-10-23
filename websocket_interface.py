#!/usr/bin/env python
import asyncio
import json

import aioredis
import websockets


class WebsocketInterface(object):
    def __init__(self):
        self.clients = {}

    async def init_redis(self):
        _redis = await aioredis.create_redis(('localhost', '6379'))
        sub = await _redis.subscribe('websocket_interface')
        return sub[0]

    async def redis_listener(self, channel):
        while await channel.wait_message():
            msg = json.loads(await channel.get(encoding='utf-8'))
            print("received message => {}".format(msg))
            asyncio.ensure_future(self.websocket_publisher(msg))

    async def init_websocket(self):
        await websockets.serve(self.websocket_handler, 'localhost', 8889)

    async def websocket_handler(self, websocket, _):
        message = json.loads(await websocket.recv())
        self.clients.setdefault(message['topic'], set()).add(websocket)
        # print(['topic {} has {} clients'.format(k, len(v)) for k, v in self.clients.items()])
        await self.websocket_consumer(websocket)

    async def websocket_consumer(self, websocket):
        while True:
            message = json.loads(await websocket.recv())
            print('someone send -> {}'.format(message))

    async def websocket_publisher(self, msg):
        targets = self.clients[msg['topic']] if msg['topic'] in self.clients else []
        # print('sending for {} in {} category'.format(len(targets), msg['topic']))
        for target in targets:
            await target.send(msg['data'])

    async def start(self):
        asyncio.ensure_future(self.init_websocket())
        ws_channel = await self.init_redis()
        asyncio.ensure_future(self.redis_listener(ws_channel))


def main():
    loop = asyncio.get_event_loop()
    server = WebsocketInterface()
    loop.run_until_complete(server.start())
    loop.run_forever()


if __name__ == '__main__':
    main()
