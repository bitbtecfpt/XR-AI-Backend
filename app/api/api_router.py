# Import `APIRouter` từ FastAPI để tạo các route (endpoint) API.
from fastapi import APIRouter

# Import module `api_chat_bot` từ thư mục `api` để sử dụng các route (endpoint) liên quan đến chatbot.z
from app.api import api_chat_bot

# Khởi tạo một router mới từ FastAPI để nhóm các route liên quan đến chatbot.
router = APIRouter()

# Include các route từ `api_chat_bot` vào router hiện tại.
router.include_router(api_chat_bot.router, tags=["chat-bot"], prefix="/chat")
