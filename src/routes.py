from datetime import timedelta

from flask import Flask
from flask import jsonify
from flask import request
from flask_cors import CORS

from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds=60)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
jwt = JWTManager(app)

URL_PREFIX = '/api/v1'

# We verify the users password here, so we are returning a fresh access token
@app.route(f'{ URL_PREFIX }/login', methods=["POST"])
def login():
    
    print(request)
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    
    if username != 'test' or password != 'test':
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity="example_user", fresh=True)
    refresh_token = create_refresh_token(identity="example_user")
    return jsonify(access_token=access_token, refresh_token=refresh_token)


# If we are refreshing a token here we have not verified the users password in
# a while, so mark the newly created access token as not fresh
@app.route(f'{ URL_PREFIX }/refresh', methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, fresh=False)
    return jsonify(access_token=access_token)


# Only allow fresh JWTs to access this route with the `fresh=True` arguement.
@app.route(f'{ URL_PREFIX }/protected', methods=["GET"])
@jwt_required(fresh=False)
def protected():
    return jsonify(foo="bar")


if __name__ == "__main__":
    app.run()