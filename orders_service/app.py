from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
import pika
import json

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.db"

db = SQLAlchemy(app)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()


@app.route("/orders", methods=["POST"])
def add_order():
    data = request.json
    new_order = Order(product_id=data["product_id"], 
                      quantity=data["quantity"])
    db.session.add(new_order)
    db.session.commit()

    send_to_queue(new_order)

    return jsonify({
        "message": "order placed"
    }), 201

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

if __name__ == "__main__":
    app.run(port=5002)