import os
import secrets
import jwt
import logging
from dotenv import load_dotenv, set_key
from flask import Flask

app = Flask(__name__)

logging.basicConfig(filename='app.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Load environment variables from .env file
load_dotenv()

def generate_secret_key():
    return secrets.token_hex(32)

def set_secret_key():
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        secret_key = generate_secret_key()
        set_key('.env', 'SECRET_KEY', secret_key)
    return secret_key

def generate_token(user_id, username, roles):
    payload = {
        'user_id': user_id,
        'username': username,
        'roles': roles
        # No expiration time
    }
    secret_key = set_secret_key()
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    set_key('.env', 'AUTHORIZED_TOKEN', token)
    logging.info(f"Token generated for user: {username}")
    return token

def get_authorized_token():
    return os.getenv('AUTHORIZED_TOKEN')

def refresh_token(token):
    try:
        secret_key = set_secret_key()
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'], options={"verify_exp": False})
        new_token = generate_token(
            user_id=decoded_token['user_id'],
            username=decoded_token['username'],
            roles=decoded_token['roles']
        )
        set_key('.env', 'AUTHORIZED_TOKEN', new_token)
        return new_token
    except Exception as e:
        logging.error(f"Error refreshing token: {e}")
        return None

def authenticate_token(token):
    authorized_token = get_authorized_token()
    if token != authorized_token:
        logging.error("Token does not match the authorized token.")
        return False, None

    try:
        secret_key = set_secret_key()
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        logging.info("Token authenticated successfully")
        return True, decoded_token
    except jwt.InvalidTokenError:
        logging.error("Invalid token.")
        return False, None
