from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
import jwt
import datetime

app = Flask(__name__)

######################## Generate RSA key pair ###########################################
def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

private_key, public_key = generate_key_pair()

######################## Key ID and expiry timestamp ######################################
kid = 'my-key-id'

def generate_expiry_timestamp():
    return datetime.datetime.utcnow() + datetime.timedelta(days=1)

expiry_timestamp = generate_expiry_timestamp()

######################## RESTful JWKS endpoint ############################################
@app.route('/jwks', methods=['GET'])
def jwks():
    if datetime.datetime.utcnow() > expiry_timestamp:
        return jsonify(error='Key has expired'), 400

    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode('utf-8')

    jwks_data = {
        "keys": [{
            "kid": kid,
            "kty": "RSA",
            "alg": "RS256",
            "use": "sig",
            "n": public_key.public_numbers().n,
            "e": public_key.public_numbers().e
        }]
    }
    return jsonify(jwks_data)

############################Authentication endpoint########################################
@app.route('/auth', methods=['POST'])
def auth():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    ############################ Mock authentication ######################################
    if username == 'userABC' and password == 'password123':
        # Introduce JWT with header kid #
        token_payload = {
            "sub": username,
            "exp": expiry_timestamp,
            "iss": "your_issuer",
            "aud": "your_audience",
        }
        token = jwt.encode(token_payload, private_key, algorithm='RS256', headers={"kid": kid})
        return jsonify(token=token.decode('utf-8'))

    return jsonify(error='Authentication failed'), 401

if __name__ == '__main__':
    app.run(port=8080)
