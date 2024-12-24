from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Cấu hình kết nối đến PostgreSQL
DATABASE_URL = (f"postgresql+psycopg2://{settings.USERNAME_DB}:"
                f"{settings.PASSWORD_DB}@{settings.HOST_DB}:{settings.PORT_DB}/{settings.NAME_DB}")

# Tạo engine
engine = create_engine(DATABASE_URL, echo=True)


# Tạo Session để giao tiếp với database
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
