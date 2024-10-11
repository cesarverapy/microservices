from flask import jsonify, request
from flask_jwt_extended import create_access_token
import os

def generate_token(username, password):
    admin_user = os.getenv('ADMIN_USERNAME')
    admin_pass = os.getenv('ADMIN_PASSWORD')

    if username == admin_user and password == admin_pass:
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Bad credentials"}), 401
