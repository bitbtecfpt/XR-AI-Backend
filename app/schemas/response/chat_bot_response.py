from pydantic import BaseModel


class ChatBotResponse(BaseModel):
    content: str
