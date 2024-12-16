import logging

import openai

from app.helper.ChatHistoryFile import ChatHistoryFile
from app.schemas.request.chat_bot_request import ChatBotRequest
from app.schemas.response.chat_bot_response import ChatBotResponse
from app.core.config import settings


class ChatBotService(object):

    def __init__(self) -> None:
        pass

    history_manager = ChatHistoryFile()

    @staticmethod
    def generate_text(request: ChatBotRequest) -> ChatBotResponse:
        try:
            # Lưu tin nhắn của người dùng vào lịch sử
            ChatBotService.history_manager.save_message(
                session_id=request.session_id,
                role="user",
                message=request.prompt
            )

            openai.api_key = settings.SECRET_KEY_GPT
            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=ChatBotService.history_manager.get_history(request.session_id) + [
                    {"role": "user", "content": request.prompt}
                ],
                temperature=1
            )

            # Lấy phản hồi từ GPT
            bot_message = response.choices[0].message.content

            # Lưu phản hồi của bot vào lịch sử
            ChatBotService.history_manager.save_message(
                session_id=request.session_id,
                role="bot",
                message=bot_message
            )

            # Trả về nội dung phản hồi
            return ChatBotResponse(content=bot_message)

        except Exception as e:
            # Log lỗi
            logging.error(f"Error during GPT request: {e}")
            raise Exception(f"Error during GPT request: {e}")
