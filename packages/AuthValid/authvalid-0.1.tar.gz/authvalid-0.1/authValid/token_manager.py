import os
import secrets
import jwt
import logging
from flask import Flask
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv, set_key

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

def get_or_generate_secret_key():
    secret_key = os.getenv('SECRET_KEY')
    if not secret_key:
        secret_key = secrets.token_hex(32)
        set_key('.env', 'SECRET_KEY', secret_key)
    return secret_key

SECRET_KEY = get_or_generate_secret_key()

app.config['AUTHORIZED_TOKEN'] = None

def generate_token(user_id, username, roles):
    stored_token = app.config['AUTHORIZED_TOKEN']
    
    if stored_token:
        try:
            decoded_token = jwt.decode(stored_token, SECRET_KEY, algorithms=['HS256'])
            logging.info(f"Valid token found for user: {username}")
            return stored_token  
        except jwt.ExpiredSignatureError:
            logging.info("Token has expired. Generating a new token.")
        except jwt.InvalidTokenError as e:
            logging.error(f"Invalid token found: {e}. Generating a new token.")
    
    payload = {
        'user_id': user_id,
        'username': username,
        'roles': roles,
        'iat': datetime.now(timezone.utc),
        'exp': datetime.now(timezone.utc) + timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    logging.info(f"New token generated: {token}")
    app.config['AUTHORIZED_TOKEN'] = token
    logging.info(f"New token generated for user: {username}")
    return token

def authenticate_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        logging.info("Token authenticated successfully")
        return True, decoded_token
    except jwt.ExpiredSignatureError:
        logging.error("Token has expired.")
        return False, None
    except jwt.InvalidTokenError as e:
        logging.error(f"Invalid token: {e}")
        return False, None