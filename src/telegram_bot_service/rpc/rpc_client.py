#!/usr/bin/env python

import asyncio
import uuid
import aiormq

class FibonacciRpcClient:

    def __init__(self, url='amqp://rmuser:rmpassword@rabbitmq/'):
        self.url = url
        self.response = None
        self.corr_id = None

#abc
    async def on_response(self, message):
        if self.corr_id == message.correlation_id:
            self.response = message.body.decode()


    async def call(self, n):
        print('i was there')
        async with aiormq.Connection(self.url) as connection:
            async with await connection.channel() as channel:
                self.response = None
                self.corr_id = str(uuid.uuid4())
                callback_queue = await channel.declare_queue(exclusive=True)
                await callback_queue.consume(self.on_response)

                await channel.basic_publish(
                    exchange='',
                    routing_key='rpc_queue',
                    properties={
                        'reply_to': callback_queue.name,
                        'correlation_id': self.corr_id,
                    },
                    body=n.encode()
                )
                print('and there')
                while self.response is None:
                    await connection.process_data_events()
                print('and there too')
                await callback_queue.cancel()
                return self.response


caller = FibonacciRpcClient()
