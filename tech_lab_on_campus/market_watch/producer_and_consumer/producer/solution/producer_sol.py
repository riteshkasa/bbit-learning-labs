import pika
import os
from producer_interface import mqProducerInterface

os.environ["AMQP_URL"] = "https://ominous-space-train-5rv5qp569vp37qg9-15672.app.github.dev/"

class mqProducer(mqProducerInterface):
    def __init__(self, routing_key: str, exchange_name: str):
        self.routing_key = routing_key
        self.exchange_name = exchange_name

        self.setupRMQConnection()

    def setupRMQConnection(self) -> None:
        # Set-up Connection to RabbitMQ service
        con_params = pika.URLParameters(os.environ["AMQP_URL"])
        connection = pika.BlockingConnection(parameters=con_params)
        # Establish Channel
        channel = connection.channel()
        # Create the exchange if not already present
        exchange = channel.exchange_declare(exchange=self.exchange_name)

    def publishOrder(self, message: str) -> None:
        # Basic Publish to Exchange
        channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=self.routing_key,
            body=message,
        )
        channel.queue_declare(queue="Queue Name")
        channel.queue_bind(
            queue= "Queue Name",
            routing_key= self.routing_key,
            exchange=self.exchange_name,
        )
        # Close Channel
        channel.close()
        # Close Connection
        connection.close()