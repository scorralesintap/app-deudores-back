from datetime import datetime
from src.infrastructure.database.base import Base
from sqlalchemy import Boolean, DateTime, Integer, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

class User(Base):

    __tablename__ = "tbl_users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    document_number: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    failed_login_attempts: Mapped[int] = mapped_column(SmallInteger, default=0, nullable=False)
    locked_until: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=datetime.now)
    updated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True, onupdate=datetime.now)
    last_login: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)