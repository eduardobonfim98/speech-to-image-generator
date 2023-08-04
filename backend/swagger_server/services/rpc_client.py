import threading
import warnings
import pika
import uuid
import os

from swagger_server.services.config import CONFIG

credentials = pika.PlainCredentials('admin', os.getenv("RABBIT_MQ_PW"))
virtual_host = CONFIG['rabbit_mq']['virtual_host']
host = CONFIG['rabbit_mq']['host']


def send_message(routing_key, payload):
    print(f"Routing key:{routing_key}. - Thread number: {threading.get_ident()}. - Payload: {payload}")
    print("First sender to the exchange 'sender' - rpc_client.py")
    corr_id = str(uuid.uuid4())
    first_connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host, credentials=credentials, virtual_host=virtual_host)
    )
    first_channel = first_connection.channel()
    first_channel.exchange_declare(exchange='sender', exchange_type='topic')
    first_channel.basic_publish(
        exchange='sender',
        routing_key=routing_key,
        properties=pika.BasicProperties(correlation_id=corr_id),
        body=payload)
    # close the connection after the message is sent, because everytime we sent a message we open a new connection
    first_connection.close()


class Receiver:

    def __init__(self, routing_key, callback_fn):
        print("Second receiver to the exchange 'response' - rpc_client.py")
        self.exchange = 'response'
        self.routing_key = routing_key
        self.callback_fn = callback_fn
        self.second_consumer_connection = None
        self.second_consumer_channel = None

        self.setup()

    def setup(self):
        self.second_consumer_connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=host, credentials=credentials, virtual_host=virtual_host)
        )
        self.second_consumer_channel = self.second_consumer_connection.channel()
        self.second_consumer_channel.exchange_declare(exchange=self.exchange, exchange_type='topic')

        self.second_consumer_channel.queue_declare(queue=self.routing_key)
        self.second_consumer_channel.queue_bind(exchange=self.exchange, queue=self.routing_key,
                                                routing_key=self.routing_key)

    def on_response(self, ch, method, props, body):
        self.callback_fn(body)

    def start_consuming(self):
        print(f"Routing key:{self.routing_key}. - Thread number: {threading.get_ident()}")
        print("start_consuming from the exchange rpc_server_response - rpc_client.py")
        try:
            self.second_consumer_channel.basic_consume(queue=self.routing_key, auto_ack=True,
                                                       on_message_callback=self.on_response)

            self.second_consumer_channel.start_consuming()

        except pika.exceptions.AMQPConnectionError:
            print("Connection lost. Reconnecting...")
            self.setup()
            self.start_consuming()

        warnings.warn("start_consuming() has finished. This should not happen.")
