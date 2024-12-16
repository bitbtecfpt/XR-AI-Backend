import enum  # Thư viện enum giúp tạo ra các enum class để quản lý các loại dữ liệu cố định

# Các thư viện FastAPI giúp xử lý HTTP requests và responses
from fastapi import Request
from fastapi.encoders import jsonable_encoder  # Dùng để chuyển đổi đối tượng Python thành dữ liệu JSON
from fastapi.responses import JSONResponse  # Dùng để trả về phản hồi JSON
from app.schemas.sche_base_response import \
    ResponseSchemaBase  # Lớp để xử lý phản hồi của hệ thống, import từ module schemas


# Định nghĩa các loại exception hệ thống bằng Enum để dễ dàng quản lý và sử dụng
class ExceptionType(enum.Enum):
    # Các exception có HTTP code, code lỗi, và message mô tả
    MS_UNAVAILABLE = 500, '990', 'The system is under maintenance, please try again later.'
    MS_INVALID_API_PATH = 500, '991', 'The system is under maintenance, please try again later.'
    DATA_RESPONSE_MALFORMED = 500, '992', 'An error occurred, please contact admin!'

    # Phương thức __new__ tự động gán giá trị cho mỗi enum
    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1  # Tính giá trị mới cho enum dựa trên số lượng enum đã có
        obj = object.__new__(cls)  # Tạo đối tượng mới cho enum
        obj._value_ = value  # Gán giá trị cho đối tượng enum
        return obj

    # Hàm khởi tạo cho mỗi exception
    def __init__(self, http_code, code, message):
        self.http_code = http_code  # Mã HTTP trả về
        self.code = code  # Mã lỗi riêng của hệ thống
        self.message = message  # Thông báo lỗi chi tiết


# Định nghĩa một exception tùy chỉnh, kế thừa từ Exception
class CustomException(Exception):
    http_code: int  # Mã HTTP trả về
    code: str  # Mã lỗi hệ thống
    message: str  # Thông báo lỗi chi tiết

    # Phương thức khởi tạo exception, có thể truyền vào mã HTTP, mã lỗi, và thông báo lỗi
    def __init__(self, http_code: int = None, code: str = None, message: str = None):
        # Nếu không truyền vào thì mặc định là 500 (Lỗi hệ thống)
        self.http_code = http_code if http_code else 500
        self.code = code if code else str(self.http_code)  # Mã lỗi mặc định bằng mã HTTP nếu không có
        self.message = message  # Thông báo lỗi


# Xử lý exception khi có lỗi xảy ra trong ứng dụng
async def http_exception_handler(request: Request, exc: CustomException):
    # Trả về phản hồi JSON với mã lỗi và thông báo chi tiết từ CustomException
    return JSONResponse(
        status_code=exc.http_code,  # Mã HTTP
        content=jsonable_encoder(ResponseSchemaBase().custom_response(exc.code, exc.message))
        # Chuyển đối tượng thành JSON
    )


# Xử lý lỗi khi validation dữ liệu không thành công
async def validation_exception_handler(request, exc):
    # Trả về phản hồi với mã lỗi 400 (Bad Request) và thông báo lỗi từ quá trình validation
    return JSONResponse(
        status_code=400,  # Mã lỗi 400 cho request không hợp lệ
        content=jsonable_encoder(ResponseSchemaBase().custom_response('400', get_validation_message(exc)))
        # Chuyển thành JSON
    )


# Xử lý các lỗi chung trong FastAPI (ví dụ: lỗi hệ thống)
async def fastapi_error_handler(request, exc):
    # Trả về phản hồi lỗi hệ thống với mã lỗi 500 (Internal Server Error)
    return JSONResponse(
        status_code=500,  # Mã lỗi 500 cho lỗi hệ thống
        content=jsonable_encoder(
            ResponseSchemaBase().custom_response('500', "An error occurred, please contact admin!"))  # Thông báo lỗi
    )


# Hàm này tạo thông báo lỗi cho trường hợp validation không thành công
def get_validation_message(exc):
    message = ""  # Khởi tạo chuỗi rỗng để chứa thông báo lỗi
    # Lặp qua tất cả các lỗi từ quá trình validation
    for error in exc.errors():
        # Cấu trúc thông báo lỗi theo định dạng '/field_name/: error_message'
        message += "/'" + str(error.get("loc")[1]) + "'/" + ': ' + error.get("msg") + ", "

    # Loại bỏ dấu phẩy thừa ở cuối chuỗi thông báo
    message = message[:-2]

    return message  # Trả về chuỗi thông báo lỗi
