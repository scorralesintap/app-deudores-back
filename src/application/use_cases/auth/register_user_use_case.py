from src.domain.value_objects.user.user_document_number import UserDocumentNumber
from src.domain.value_objects.user.user_password import UserPassword
from src.application.dtos.users.create_user_dto import CreateUserDto
from src.application.dtos.users.create_user_response_dto import CreateUserResponseDto
from src.domain.ports.ports_in.auth import IRegisterUserUseCase
from src.domain.models.user import User as DomainUser
from src.domain.ports.ports_out import IUserRepository

class RegisterUserUseCase(IRegisterUserUseCase):

    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    async def create(self, create_user_dto: CreateUserDto) -> CreateUserResponseDto:

        existing_user = await self.user_repository.get_by_document_number(create_user_dto.document_number)
        if existing_user:
            raise Exception("El documento ya está registrado")

        document_number = UserDocumentNumber(create_user_dto.document_number)
        password_hashed = UserPassword(create_user_dto.password)

        user_domain = DomainUser(
            document_number = document_number,
            password = password_hashed
        )

        user = await self.user_repository.create(user_domain)

        return CreateUserResponseDto(
            id = user.id,
            document_number = user.document_number.value
        )