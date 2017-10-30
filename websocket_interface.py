#!/usr/bin/env python
import asyncio
import json

import aioredis
import websockets

HOST = 'localhost'
REDIS_PORT = '6379'
WEBSOCKET_PORT = 8889


class WebsocketInterface(object):
    def __init__(self):
        self.clients = {}

    async def init_redis(self):
        _redis = await aioredis.create_redis((HOST, REDIS_PORT))
        sub = await _redis.subscribe('websocket_interface')
        return sub[0]

    async def redis_listener(self, channel):
        while await channel.wait_message():
            msg = json.loads(await channel.get(encoding='utf-8'))
            print("received message => {}".format(msg))
            asyncio.ensure_future(self.websocket_publisher(msg))

    async def init_websocket(self):
        await websockets.serve(self.websocket_handler, HOST, WEBSOCKET_PORT)

    async def websocket_handler(self, websocket, _):
        message = json.loads(await websocket.recv())
        if self.is_message_valid(message):
            self.websocket_client_handler(message['action'], message['topic'], websocket)
            await self.websocket_consumer(message['topic'], websocket)

    async def websocket_consumer(self, topic, websocket):
        new_topic = None
        try:
            while True:
                message = json.loads(await websocket.recv())
                if self.is_message_valid(message):
                    new_topic = message['topic']
                    self.websocket_client_handler(message['action'], new_topic, websocket)
        except websockets.exceptions.ConnectionClosed:
            self.clients[new_topic or topic].remove(websocket)

    @staticmethod
    def is_message_valid(message):
        return all(keys in message for keys in ['action', 'topic']) and message['action'] in ['subscribe', 'unsubscribe'] 

    def websocket_client_handler(self, action, topic, websocket):
        if action == 'subscribe':
            self.clients.setdefault(topic, set()).add(websocket)
        else:
            self.clients[topic].remove(websocket)

    async def websocket_publisher(self, msg):
        targets = self.clients[msg['topic']] if msg['topic'] in self.clients else []
        for target in targets:
            await target.send(msg['data'])

    async def start(self):
        asyncio.ensure_future(self.init_websocket())
        ws_channel = await self.init_redis()
        asyncio.ensure_future(self.redis_listener(ws_channel))


def main():
    loop = asyncio.get_event_loop()
    server = WebsocketInterface()
    asyncio.ensure_future(server.start())
    loop.run_forever()


if __name__ == '__main__':
    main()
