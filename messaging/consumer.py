import pika
import json

# Correct callback function for consuming messages
def callback(ch, method, properties, body):
    data = json.loads(body)
    # Fixed string quotation issues
    print(f"received order for product {data['product_id']} with quantity {data['quantity']}")

    process_order(data)

# Processing logic for the order
def process_order(order_data):
    product_id = order_data["product_id"]
    quantity = order_data["quantity"]

    print(f"processing order for {product_id} with quantity {quantity}")

# Start the consumer to listen to the RabbitMQ queue
def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Corrected queue name
    channel.queue_declare(queue="order_queue")
    
    # Fixed the queue name and added the correct callback function
    channel.basic_consume(queue="order_queue", on_message_callback=callback, auto_ack=True)

    print("[*] waiting for messages. to exit press ctrl + c")
    channel.start_consuming()

if __name__ == "__main__":
    start_consumer()
