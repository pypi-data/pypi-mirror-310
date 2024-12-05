from flask import Flask
import os
import secrets
import jwt
import logging
from dotenv import load_dotenv, set_key
from pathlib import Path
from datetime import datetime, timedelta

app = Flask(__name__)

logging.basicConfig(filename='app.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv()

def generate_secret_key():
    return secrets.token_hex(32)

def set_secret_key():
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        secret_key = generate_secret_key()
        set_key('.env', 'SECRET_KEY', secret_key)
    return secret_key

def generate_token(user_id, username, roles, expiration_minutes=60):
    payload = {
        'user_id': user_id,
        'username': username,
        'roles': roles,
        'exp': datetime.utcnow() + timedelta(minutes=expiration_minutes)
    }
    secret_key = set_secret_key()
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    set_key('.env', 'AUTHORIZED_TOKEN', token)
    logging.info(f"Token generated for user: {username}")
    return token

def refresh_token(token):
    try:
        secret_key = set_secret_key()
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'], options={"verify_exp": False})
        new_token = generate_token(
            user_id=decoded_token['user_id'],
            username=decoded_token['username'],
            roles=decoded_token['roles']
        )
        return new_token
    except Exception as e:
        logging.error(f"Error refreshing token: {e}")
        return None

def authenticate_token(token):
    try:
        secret_key = set_secret_key()
        decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        logging.info("Token authenticated successfully")
        return True, decoded_token
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired.")
        return False, None
    except jwt.InvalidTokenError:
        logging.error("Invalid token.")
        return False, None