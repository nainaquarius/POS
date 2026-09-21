from pwdlib import PasswordHash
from app.config import settings
from datetime import datetime, timezone, timedelta
from jose import jwt

password_hash = PasswordHash.recommended()

def hash_password(password: str):
  return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str):
  return password_hash.verify(plain_password, hashed_password)

def create_access_token(data: dict):
  to_encode = data.copy()

  to_expire = datetime.now(timezone.utc) + timedelta(
    minutes=settings.access_token_expire_minutes
  )

  to_encode.update({"exp" : to_expire})

  encoded_token = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

  return encoded_token