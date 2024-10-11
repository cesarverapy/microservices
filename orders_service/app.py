from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from models import db, Order
from services import send_to_queue
from dotenv import load_dotenv
from auth import generate_token 
import os

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("SECRET_KEY")

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    return generate_token(username, password)

@app.route("/orders", methods=["POST"])
@jwt_required()
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

if __name__ == "__main__":
    app.run(port=5002)