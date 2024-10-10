from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///products.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()


# get products

@app.route("/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, 
                     "name": p.name, 
                     "price": p.price}
                     for p in products])

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