import re

from datetime import datetime as dt

from app.helper.exception_handler import CustomException, ExceptionType


def validate_email(value: str) -> str:
    """
    Validate email format.
    """
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(pattern, value):
        raise CustomException(ExceptionType.VALIDATION_ERROR, "Invalid email format")
    return value


def validate_password(value: str) -> str:
    """
    Validate password complexity.
    """
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$"
    if not re.match(pattern, value):
        raise CustomException(ExceptionType.VALIDATION_ERROR, "Password must contain at least 1 uppercase letter, "
                                                              "1 lowercase letter, 1 digit, and have at least 8 "
                                                              "characters")
    return value


def validate_birth_year(value: int) -> int:
    current_year = dt.now().year
    if (current_year - value) < 18:
        raise ValueError('User must be at least 18 years old')
    return value


def validate_name(value: str) -> str:
    """
    Validate name ko chứa các ký hiệu đặc biệt
        ví dụ: @, #, $, %, ^, &, *, (, ), [, ], {, }, <, >, /, \\, |, ~, `, !, ", ', :, ;, ?, .
    """
    pattern = r"^[a-zA-Z0-9_ ]+$"
    if not re.match(pattern, value):
        raise ValueError('Name must not contain special characters')
    return value
