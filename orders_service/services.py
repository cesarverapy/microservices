import pika
import json

def send_to_queue(order):
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="order_queue")
    message = {
        "product_id": order.product_id,
        "quantity": order.quantity
    }
    channel.basic_publish(exchange="", routing_key="order_queue", body=json.dumps(message))
    connection.close()