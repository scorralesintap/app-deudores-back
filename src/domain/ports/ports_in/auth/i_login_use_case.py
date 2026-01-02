from abc import ABC, abstractmethod
from src.domain.models.user import User
from src.application.dtos.auth.login_dto import LoginDto

class ILoginUseCase(ABC):

    @abstractmethod
    def login(self, login_dto: LoginDto) -> User:
        pass