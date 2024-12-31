from typing import Any
# Import `Any` từ module `typing`, cho phép khai báo kiểu dữ liệu có thể là bất kỳ kiểu nào, không giới hạn. Điều này
# giúp tăng tính linh hoạt cho đoạn mã.

from fastapi import APIRouter, Depends, Request
# Import `APIRouter` từ FastAPI để tạo các route (endpoint) API.
# `Depends` dùng để quản lý các dependency trong route, giúp inject các đối tượng hoặc dịch vụ vào hàm xử lý.

from app.core.security import JWTBearer, role_required
# Import `JWTBearer` từ module `security` trong ứng dụng, đây là middleware để xác thực token JWT từ header của yêu
# cầu. Middleware này sẽ giúp bảo vệ các endpoint cần xác thực. `role_required` là một decorator để kiểm tra vai trò
# của người dùng, đảm bảo chỉ những người dùng có quyền mới được truy

from app.helper.exception_handler import CustomException, ExceptionType
# Import `CustomException` từ module `exception_handler` trong ứng dụng, dùng để tạo và xử lý lỗi tùy chỉnh,
# giúp ứng dụng dễ dàng quản lý các ngoại lệ.

from app.schemas.sche_base_response import DataResponse
# Import `DataResponse` từ module `sche_base_response`, đây là schema định dạng phản hồi từ API.
# `DataResponse` chứa các thông tin như dữ liệu trả về và mã trạng thái của phản hồi.

from app.schemas.response.chat_bot_response import ChatBotResponse
# Import `ChatBotResponse` từ module `chat_bot_response`, đây là schema dùng để định dạng dữ liệu phản hồi của chatbot.
# Thông thường, schema này chứa các trường như câu trả lời từ chatbot và các thông tin khác liên quan đến phản hồi.

from app.schemas.request.chat_bot_request import ChatBotRequest
# Import `ChatBotRequest` từ module `chat_bot_request`, schema này định nghĩa cấu trúc yêu cầu mà người dùng gửi đến
# API. Schema này thường chứa các trường như câu hỏi của người dùng mà chatbot cần trả lời.

from app.service.chat_bot_service import ChatBotService
# Import `ChatBotService` từ module `chat_bot_service`, dịch vụ này xử lý các logic liên quan đến chatbot,
# chẳng hạn như sinh ra câu trả lời từ dữ liệu yêu cầu.

from app.helper.constant import roleEnum

router = APIRouter()
# Khởi tạo một router mới từ FastAPI để nhóm các route liên quan đến chatbot.
# Router giúp phân chia các chức năng trong API một cách có tổ chức và dễ dàng mở rộng.


@router.post("", response_model=DataResponse[ChatBotResponse], dependencies=[Depends(JWTBearer())])
# Định nghĩa một endpoint HTTP `POST` cho route gốc (""), có nhiệm vụ nhận yêu cầu từ người dùng và trả về dữ liệu
# depend on JWTBearer middleware có tác dụng xác thực token JWT từ header của yêu cầu.
# dưới dạng `DataResponse` với dữ liệu là `ChatBotResponse`. `response_model` giúp định nghĩa cấu trúc của dữ liệu
@role_required([roleEnum.USER.value])
# Sử dụng decorator `role_required` để kiểm tra vai trò của người dùng, chỉ những người dùng có vai trò là
# "admin" hoặc phản hồi.
async def send(request: Request, chat_bot_service: ChatBotService = Depends()) -> Any:
    """
    Đây là hàm xử lý cho endpoint `POST`. Tham số `request` nhận dữ liệu yêu cầu từ người dùng dưới dạng
    `ChatBotRequest`. `chat_bot_service` là một dependency được inject vào hàm xử lý bằng cách sử dụng
    `Depends()`. Dịch vụ này sẽ chịu trách nhiệm tạo câu trả lời cho chatbot.
    """

    try:
        # Bắt đầu một khối `try`, nơi bạn sẽ thực hiện các thao tác có thể gây ra lỗi và cần phải xử lý.

        # Parse dữ liệu từ request
        body = await request.json()
        request = ChatBotRequest(**body)

        # Gọi dịch vụ sinh câu trả lời
        response = chat_bot_service.generate_text(request)

        # Trả về phản hồi thành công
        return DataResponse().success_response(data=response)

    except Exception as e:
        # Nếu có lỗi xảy ra trong khối `try`, khối `except` sẽ bắt lỗi đó.

        raise CustomException(ExceptionType.BAD_REQUEST, message=str(e))
        # Ném ra một lỗi tùy chỉnh (`CustomException`) với mã lỗi HTTP 400 (Bad Request) và thông điệp lỗi là chi
        # tiết của lỗi từ ngoại lệ `e`. Điều này giúp gửi thông tin lỗi rõ ràng và dễ hiểu cho người dùng hoặc hệ thống.
