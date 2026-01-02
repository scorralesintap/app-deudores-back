from abc import ABC, abstractmethod
from src.application.dtos.users.create_user_dto import CreateUserDto
from src.application.dtos.users.create_user_response_dto import CreateUserResponseDto

class IRegisterUserUseCase(ABC):

    @abstractmethod
    def create(self, createUserDto: CreateUserDto) -> CreateUserResponseDto:
        pass