from fastapi import APIRouter

from app.api import api_chat_bot

router = APIRouter()

router.include_router(api_chat_bot.router, tags=["chat-bot"], prefix="/chat")
