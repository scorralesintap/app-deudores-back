from abc import ABC, abstractmethod
from src.domain.models.user import User

class ILoginUseCase(ABC):

    @abstractmethod
    def login(self, document_number: int, password: str) -> User:
        pass