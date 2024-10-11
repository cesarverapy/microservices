from flask import Flask, jsonify, request
from models import db, Product
from flask_jwt_extended import JWTManager, jwt_required
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

# Login route to generate token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    return generate_token(username, password)

@app.route("/products", methods=["GET"])
@jwt_required()
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, 
                     "name": p.name, 
                     "price": p.price}
                     for p in products])

@app.route("/products", methods=["POST"])
@jwt_required()
def add_product():
    data = request.json
    new_product = Product(name=data["name"],
                          price=data["price"])
    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "message": "product added"
    }), 201

if __name__ == "__main__":
    app.run(port=5001)