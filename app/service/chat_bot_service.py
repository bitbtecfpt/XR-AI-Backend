import logging

from app.helper.connect_gpt import ConnectGPT
from app.schemas.request.chat_bot_request import ChatBotRequest
from app.schemas.response.chat_bot_response import ChatBotResponse


class ChatBotService(object):

    def __init__(self) -> None:
        pass

    @staticmethod
    def generate_text(request: ChatBotRequest) -> ChatBotResponse:
        try:
            bot_message = ConnectGPT.connect(request)
            # Trả về nội dung phản hồi
            return ChatBotResponse(content=bot_message)

        except Exception as e:
            # Log lỗi
            logging.error(f"Error during GPT request: {e}")
            raise Exception(f"Error during GPT request: {e}")
