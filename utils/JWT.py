import jwt
from jwt.exceptions import ExpiredSignatureError
from datetime import datetime, timedelta

def create_token(body):
  token = jwt.encode({**body, 'exp': datetime.utcnow() + timedelta(minutes=1)}, 'secret', algorithm='HS256')
  return token

def decode_token(token):
  try:
    body = jwt.decode(token, 'secret', algorithms=['HS256'])
    return body
  except ExpiredSignatureError:
    return False

def verify_token(body):
  current_time = datetime.utcnow()

  try:
    if 'exp' in body and body.get('exp') >= current_time:
      return True
    else: 
      return False
  except ExpiredSignatureError:
    return "Token expirado", 401