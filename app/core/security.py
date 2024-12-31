from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Callable
from functools import wraps
from app.core.JWT_security import verify_jwt_token
from app.helper.constant import roleEnum

# Danh sách các endpoint cho phép anonymous access
PUBLIC_ACCESS_ENDPOINTS = [
    "/public",
    "/authentication/*",
    "/docs",  # Nếu bạn muốn mở tài liệu Swagger
    "/open-api",
]


# Middleware để lấy token từ header Authorization
class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> str | None:
        # Cho phép truy cập công khai đến các endpoint được định nghĩa
        if any(request.url.path.startswith(endpoint) for endpoint in PUBLIC_ACCESS_ENDPOINTS):
            return None

        credentials: HTTPAuthorizationCredentials = await super().__call__(request)
        if credentials:
            if credentials.scheme != "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            return credentials.credentials
        raise HTTPException(status_code=403, detail="Invalid authorization header.")


def role_required(required_roles: List[roleEnum]) -> Callable:
    def decorator(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Lấy request từ kwargs
            request: Request = kwargs.get("request")
            if not request:
                raise HTTPException(status_code=400, detail="Request object is missing.")

            # Lấy token từ header Authorization
            token = request.headers.get("Authorization")
            if not token:
                raise HTTPException(status_code=401, detail="Authorization header is missing.")

            try:
                # Loại bỏ tiền tố "Bearer " từ token
                if token.startswith("Bearer "):
                    token = token.replace("Bearer ", "", 1)

                # Xác minh JWT token
                payload = verify_jwt_token(token)

                # Lấy vai trò của người dùng từ payload
                user_roles = payload.get("author", [])

                # Kiểm tra vai trò của người dùng có nằm trong danh sách vai trò yêu cầu
                if not any(user_roles for _ in required_roles):
                    raise HTTPException(status_code=403, detail="Insufficient permissions.")

                # Gọi hàm mục tiêu
                return await func(*args, **kwargs)

            except HTTPException as e:
                raise e
            except Exception as e:
                raise HTTPException(status_code=401, detail=f"Token validation failed: {str(e)}")

        return wrapper

    return decorator
