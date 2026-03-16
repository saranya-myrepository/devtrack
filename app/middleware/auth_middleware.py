from functools import wraps
from flask import request, jsonify
from app.utils.jwt_utils import verify_token


def token_required(f):

    @wraps(f)   
    def decorated(*args, **kwargs):

        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            token = request.cookies.get("token") 

        if not token:
            return jsonify({"message": "Token is missing"}), 401

        decoded = verify_token(token)

        if "error" in decoded:
            return jsonify({"message": decoded["error"]}), 401

        return f(decoded, *args, **kwargs)

    return decorated