from datetime import timedelta, timezone, datetime

import jwt
from pwdlib import PasswordHash

from fastapi import HTTPException, status

from .config import settings

password_hash = PasswordHash.recommended()


# hash password function
def hash_password(password) -> str:
    return password_hash.hash(password)


# check input password
def verify_password(plain_password, hashed_password) -> bool:
    return password_hash.verify(plain_password, hashed_password)


# generate access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt.key, algorithm=settings.jwt.algorithm)
    return encoded_jwt


# decode input token
def decode_token(token) -> dict:
    try:
        data = jwt.decode(token, settings.jwt.key, algorithms=[settings.jwt.algorithm])
    except jwt.DecodeError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    return data