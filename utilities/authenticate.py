import jwt
import datetime
import base64
import os
from utilities.ENV import jwtSecret

def authenticate_token(token: str):
    if not token or len(token.split(".")) != 3:
        raise Exception("Token is missing or malformed")

    SECRET_KEY = jwtSecret
    ALGORITHM = "HS256"

    # Fix padding issue
    missing_padding = len(SECRET_KEY) % 4
    if missing_padding:
        SECRET_KEY += "=" * (4 - missing_padding)

    # print("Secret Key after Base 64:", SECRET_KEY)
    SECRET_KEY_DECODE = base64.b64decode(SECRET_KEY)
    # print("Secret Key Decode after Base 64:", SECRET_KEY_DECODE)

    try:
        # Decode without verifying to check expiration
        unverified_payload = jwt.decode(token, options={"verify_signature": False})
        exp_time = datetime.datetime.utcfromtimestamp(unverified_payload["exp"])
        current_time = datetime.datetime.utcnow()

        if current_time > exp_time:
            raise jwt.ExpiredSignatureError("Token has expired")

        # Now verify the signature
        payload = jwt.decode(token, SECRET_KEY_DECODE, algorithms=[ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError as e:
        raise Exception("Token has expired")
    except jwt.InvalidSignatureError:
        raise Exception("Invalid token signature")
    except jwt.DecodeError:
        raise Exception("Invalid Token")
    except Exception as e:
        raise Exception(f"Unknown error during token validation: {str(e)}")
