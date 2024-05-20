import jwt

from typing import Dict
from fastapi import HTTPException
from config import SERVICE_SECRET_KEY, SERVICE_SECRET_ALGORITHM, CONFIRMATION_TOKEN_TTL
from datetime import datetime, timedelta


def decode_jwt(token: str):
    try:

        return jwt.decode(
            jwt=token,
            key=SERVICE_SECRET_KEY,
            algorithms=[SERVICE_SECRET_ALGORITHM],
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")


def encode_jwt(payload: Dict):

    payload["exp"] = int(
        (datetime.now() + timedelta(seconds=CONFIRMATION_TOKEN_TTL)).timestamp()
    )

    return jwt.encode(
        payload=payload,
        key=SERVICE_SECRET_KEY,
        algorithm=SERVICE_SECRET_ALGORITHM,
    )
