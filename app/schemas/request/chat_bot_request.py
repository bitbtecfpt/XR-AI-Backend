from pydantic import BaseModel


class ChatBotRequest(BaseModel):
    prompt: str
    session_id: int = 1
