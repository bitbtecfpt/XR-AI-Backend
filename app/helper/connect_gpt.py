import openai

from app.core.config import settings
from app.helper.chat_history_file import ChatHistoryFile
from app.schemas.request.chat_bot_request import ChatBotRequest


class ConnectGPT:
    history_manager = ChatHistoryFile()

    @staticmethod
    def connect(request: ChatBotRequest) -> str:
        # Lưu tin nhắn của người dùng vào lịch sử
        ConnectGPT.history_manager.save_message(
            session_id=request.session_id,
            role="user",
            message=request.prompt
        )

        openai.api_key = settings.SECRET_KEY_GPT
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=ConnectGPT.history_manager.get_history(request.session_id) + [
                {"role": "user", "content": request.prompt}
            ],
            temperature=1
        )

        # Lấy phản hồi từ GPT
        bot_message = response.choices[0].message.content

        # Lưu phản hồi của bot vào lịch sử
        ConnectGPT.history_manager.save_message(
            session_id=request.session_id,
            role="bot",
            message=bot_message
        )

        return bot_message
