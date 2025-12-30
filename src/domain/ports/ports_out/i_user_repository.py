from abc import ABC, abstractmethod
from typing import Optional
from src.domain.models.user import User
from datetime import datetime

class IUserRepository(ABC):

    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_document_number(self, document_number: str) -> Optional[User]:
        pass

    @abstractmethod
    def update_failed_attempts(self, user: User, attempts: int, locked_until: datetime | None = None) -> None:
        pass

    @abstractmethod
    def update_last_login(self, user: User) -> None:
        pass