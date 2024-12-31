from pydantic import BaseModel, field_validator
from app.helper.constant import genderEnum
from app.helper.validators import validate_email, validate_password, validate_birth_year, validate_name


class BaseRequest(BaseModel):
    email: str  # Pydantic EmailStr for email validation
    password: str  # Pydantic field for string (password)

    @field_validator('password')
    def validate_password(cls, value):
        return validate_password(value)  # Use the imported password validation function

    @field_validator('email')
    def validate_email(cls, value):
        return validate_email(value)  # Use the imported email validation function


class AuthenticationRequest(BaseRequest):
    pass


class RegisterRequest(BaseRequest):
    name: str
    gender: genderEnum
    birth_year: int
    trans_id: str

    @field_validator('birth_year')
    def validate_birth_year(cls, value):
        return validate_birth_year(value)

    @field_validator('name')
    def validate_name(cls, value):
        return validate_name(value)
