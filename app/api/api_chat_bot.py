from typing import Any

from fastapi import APIRouter, Depends

from app.helper.exception_handler import CustomException
from app.schemas.sche_base_response import DataResponse
from app.schemas.response.chat_bot_response import ChatBotResponse
from app.schemas.request.chat_bot_request import ChatBotRequest
from app.service.chat_bot_service import ChatBotService

router = APIRouter()


@router.post("", response_model=DataResponse[ChatBotResponse])
def send(request: ChatBotRequest, chat_bot_service: ChatBotService = Depends()) -> Any:
    try:
        response = chat_bot_service.generate_text(request)
        return DataResponse().success_response(data=response)
    except Exception as e:
        raise CustomException(http_code=400, code='400', message=str(e))
