# websocket_interface
Requirements:
  -Redis server
  -Python3
    -aioredis (python module)
    -websockets (python module)

Introduction:
A simple microservice to publish messages through a websocket server. The websocket_interface is a standalone python process that listens to both Redis and Websocket in order to publish the messages to a specified group of clients through websocket. 

How to use:
First, Websocket clients should subscribe to their desired topics by sending messages with 'topic' as the key, e.g:
  let message = {'topic': 'KnockKnockNeo'};
  websocket.send(message);

Then, to send the a message to all subscribers of 'KnockKnockNeo' you only need to publish the message with desired topic to the specific Redis channel that websocket_interface listens to. e.g:
  message = {'topic': 'KnockKnockNeo', data: 'humans are viruses'}
  _redis.publish('websocket_interface_channel', message)
