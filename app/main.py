# Import thư viện Uvicorn để chạy ứng dụng FastAPI
import uvicorn

# Import FastAPI, framework để xây dựng API
from fastapi import FastAPI

# Import các cài đặt từ module config trong thư mục core
from app.core.config import settings

# Import router từ module api_router trong thư mục api
from app.api.api_router import router

# Import CORSMiddleware để xử lý Cross-Origin Resource Sharing (CORS)
from fastapi.middleware.cors import CORSMiddleware

from app.model.models import create_tables
# Import Custom Exception Handler
from app.helper.exception_handler import CustomException, http_exception_handler


def get_application() -> FastAPI:
    """
    Tạo và cấu hình ứng dụng FastAPI.
    Hàm này khởi tạo một instance của FastAPI, thêm middleware cho CORS,
    include router và xử lý exception.
    Returns:
        FastAPI: Instance của ứng dụng FastAPI đã được cấu hình.
    """
    # Khởi tạo instance của FastAPI với các cài đặt từ settings
    application = FastAPI(
        title=settings.PROJECT_NAME,  # Thiết lập tiêu đề cho ứng dụng
        docs_url=f"{settings.API_PREFIX}/docs",  # Đường dẫn đến tài liệu Swagger UI
        redoc_url=f"{settings.API_PREFIX}/re-docs",  # Đường dẫn đến tài liệu ReDoc
        openapi_url=f"{settings.API_PREFIX}/openapi.json",  # Đường dẫn đến OpenAPI schema
    )

    # Thêm middleware CORS để cho phép các request từ các origin khác nhau
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],  # Danh sách các origin được phép
        allow_credentials=True,  # Cho phép gửi credentials (cookies, authorization headers)
        allow_methods=["*"],  # Cho phép tất cả các phương thức HTTP
        allow_headers=["*"],  # Cho phép tất cả các headers
    )

    # Thêm middleware cho database session nếu cần (đã bị comment)
    # if hasattr(settings, 'DATABASE_URL') and settings.DATABASE_URL:
    #     # Đảm bảo rằng có database_url trong settings nếu bạn cần kết nối cơ sở dữ liệu
    #     # application.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)
    #     pass

    # Include router vào ứng dụng với prefix được chỉ định từ settings
    application.include_router(router, prefix=settings.API_PREFIX)

    # Xử lý Custom Exception với handler tùy chỉnh
    application.add_exception_handler(CustomException, http_exception_handler)

    # Trả về instance của ứng dụng FastAPI
    return application


create_tables()
# Khởi tạo ứng dụng FastAPI bằng cách gọi hàm get_application()
app = get_application()

# Chạy ứng dụng Uvicorn khi file được thực thi trực tiếp
if __name__ == '__main__':
    # Chạy ứng dụng FastAPI sử dụng Uvicorn
    # host="0.0.0.0" cho phép truy cập từ bất kỳ địa chỉ IP nào
    # port=8000 chỉ định cổng chạy ứng dụng
    uvicorn.run(app, host="0.0.0.0", port=8000)
