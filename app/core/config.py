import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from typing import List

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
load_dotenv(os.path.join(BASE_DIR, '.env'))


class Settings(BaseSettings):
    PROJECT_NAME: str = os.getenv('PROJECT_NAME', 'Default Project Name')  # Default value if not set
    SECRET_KEY_GPT: str = os.getenv('OPENAI_SECRET_KEY', '')
    API_PREFIX: str = os.getenv('API_PREFIX', '')
    HOST: str = os.getenv('HOST', 'localhost')
    PORT: int = os.getenv('PORT', 8000)
    BACKEND_CORS_ORIGINS: List[str] = ['*']  # List of origins
    DATABASE_URL: str = os.getenv('SQL_DATABASE_URL', '')
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 60 * 60 * 24 * 7  # Token expired after 7 days
    SECURITY_ALGORITHM: str = 'HS256'
    LOGGING_CONFIG_FILE: str = os.path.join(BASE_DIR, 'logging.ini')


# Create settings instance
settings = Settings()
