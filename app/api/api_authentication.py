import logging
from typing import Any
from fastapi import APIRouter, Depends

from app.db.config_sql import get_db
from app.helper.exception_handler import CustomException, ExceptionType
from app.schemas.request.authentication_request import RegisterRequest, AuthenticationRequest
from app.schemas.response.authentication_response import AuthenticationResponse
from app.schemas.sche_base_response import DataResponse
from app.service.authentication_service import AuthenticationService

# Khởi tạo router
router = APIRouter()


@router.post("/register", response_model=DataResponse, tags=["Authentication"])
def register(request: RegisterRequest, db_session=Depends(get_db)) -> Any:
    """
    API đăng ký người dùng.
    """
    try:
        auth_service = AuthenticationService(db_session)
        auth_service.register(request)

        return DataResponse().success_response(data=None)
    except Exception as e:
        logging.error(e)
        raise CustomException(ExceptionType.BAD_REQUEST, message=str(e))


@router.post("", response_model=DataResponse[AuthenticationResponse], tags=["Authentication"])
def authentication(request: AuthenticationRequest, db_session=Depends(get_db)) -> Any:
    """
    API xác thực người dùng.
    """
    try:
        auth_service = AuthenticationService(db_session)
        response = auth_service.authentication(request)

        return DataResponse[AuthenticationResponse]().success_response(data=response)
    except Exception as e:
        raise CustomException(ExceptionType.BAD_REQUEST, message=str(e))


@router.post("/refresh-token", response_model=DataResponse[AuthenticationResponse], tags=["Authentication"])
def refresh_token(request: AuthenticationRequest, db_session=Depends(get_db)) -> Any:
    """
    API refresh token.
    """
    try:
        auth_service = AuthenticationService(db_session)
        response = auth_service.refresh_token(request)

        return DataResponse[AuthenticationResponse]().success_response(data=response)
    except Exception as e:
        logging.error(e)
        raise CustomException(ExceptionType.BAD_REQUEST, message=str(e))


@router.post("/logout", response_model=DataResponse, tags=["Authentication"])
def logout(request: AuthenticationRequest, db_session=Depends(get_db)) -> Any:
    """
    API logout.
    """
    try:
        auth_service = AuthenticationService(db_session)
        auth_service.logout(request)

        return DataResponse().success_response(data=None)
    except Exception as e:
        logging.error(e)
        raise CustomException(ExceptionType.BAD_REQUEST, message=str(e))


@router.post("/change-password", response_model=DataResponse, tags=["Authentication"])
def change_password(request: AuthenticationRequest, db_session=Depends(get_db)) -> Any:
    """
    API đổi mật khẩu.
    """
    try:
        auth_service = AuthenticationService(db_session)
        auth_service.change_password(request)

        return DataResponse().success_response(data=None)
    except Exception as e:
        logging.error(e)
        raise CustomException(ExceptionType.BAD_REQUEST, message=str(e))


@router.post("/forgot-password", response_model=DataResponse, tags=["Authentication"])
def forgot_password(request: AuthenticationRequest, db_session=Depends(get_db)) -> Any:
    """
    API quên mật khẩu.
    """
    try:
        auth_service = AuthenticationService(db_session)
        auth_service.forgot_password(request)

        return DataResponse().success_response(data=None)
    except Exception as e:
        logging.error(e)
        raise CustomException(ExceptionType.BAD_REQUEST, message=str(e))
