import pika
import json

def callback(ch, method, properties, body):
    data = json.loads(body)
    print(f"received order for product {data['product_id']} with quantity {data['quantity']}")

    process_order(data)

def process_order(order_data):
    product_id = order_data["product_id"]
    quantity = order_data["quantity"]

    print(f"processing order for {product_id} with quantity {quantity}")

def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.queue_declare(queue="order_queue")
    
    channel.basic_consume(queue="order_queue", on_message_callback=callback, auto_ack=True)

    print("[*] waiting for messages. to exit press ctrl + c")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
