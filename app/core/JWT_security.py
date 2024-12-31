import jwt
import datetime

from typing import Optional
from app.core.config import settings
from app.helper.constant import roleEnum

# Secret key dùng để mã hóa và giải mã JWT
JWT_SECRET_KEY = settings.JWT_SECRET_KEY
JWT_ALGORITHM = settings.JWT_ALGORITHM

# Thời gian hết hạn của token
JWT_EXPIRATION_TIME = 3600  # 1 hour


# Function để tạo JWT token
def create_jwt_token(user_id: int, email: str) -> str:
    """
    Tạo JWT token cho người dùng.

    Args:
        user_id (int): ID người dùng.
        email (str): Email người dùng.

    Returns:
        str: JWT token.
    """
    payload = {
        "user_id": user_id,
        "email": email,
        "author": roleEnum.USER.value,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=JWT_EXPIRATION_TIME)
    }

    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token


# Function để xác minh JWT token
def verify_jwt_token(token: str) -> Optional[dict]:
    """
    Xác minh JWT token.

    Args:
        token (str): JWT token.

    Returns:
        dict: Payload của token nếu hợp lệ, None nếu không hợp lệ.
    """
    try:
        decoded_token = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return decoded_token
    except jwt.ExpiredSignatureError:
        print("Token has expired.")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None
