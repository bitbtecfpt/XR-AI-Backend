import logging
from typing import Any

from fastapi import APIRouter, Request, Depends

from app.helper.exception_handler import CustomException, ExceptionType
from app.schemas.request.otp_request import OtpSendRequest, OtpVerifyRequest
from app.schemas.response.otp_response import OtpResponse
from app.schemas.sche_base_response import DataResponse
from app.service.otp_service import OtpService

router = APIRouter()


@router.post("/request", response_model=DataResponse, tags=["OTP"])
async def request_otp(request: Request, otp_service: OtpService = Depends()) -> Any:
    """
    Request OTP
    """
    try:
        body = await request.json()
        request = OtpSendRequest(**body)
        otp_service.send_email_otp(request)
        return DataResponse[OtpResponse]().success_response(data=None)
    except Exception as e:
        logging.error(e)
        raise CustomException(ExceptionType.BAD_REQUEST, message=str(e))


@router.post("/verify", response_model=DataResponse[OtpResponse], tags=["OTP"])
async def verify_otp(request: Request, otp_service: OtpService = Depends()) -> Any:
    """
    Verify OTP
    """
    try:
        body = await request.json()
        request = OtpVerifyRequest(**body)
        response = otp_service.verify_otp(request)
        return DataResponse[OtpResponse]().success_response(data=response)
    except Exception as e:
        logging.error(e)
        raise CustomException(ExceptionType.BAD_REQUEST, message=str(e))
