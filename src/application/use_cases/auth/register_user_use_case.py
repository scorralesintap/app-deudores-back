from src.domain.value_objects.user.user_password import UserPassword
from src.application.dtos.users.create_user_dto import CreateUserDto
from src.application.dtos.users.create_user_response_dto import CreateUserResponseDto
from src.domain.ports.ports_in.i_register_user_use_case import IRegisterUserUseCase
from src.domain.models.user import User as DomainUser
from src.domain.ports.ports_out import IUserRepository

class RegisterUserUseCase(IRegisterUserUseCase):

    def __init__(self, IUserRepository: IUserRepository):
        self.user_repository = IUserRepository

    async def create(self, createUserDto: CreateUserDto) -> CreateUserResponseDto:

        existing_user = await self.user_repository.get_by_document_number(createUserDto.document_number)
        if existing_user:
            raise Exception("El documento ya está registrado")

        password_hashed = UserPassword(createUserDto.password)

        userDomain = DomainUser(
            document_number=createUserDto.document_number,
            password=password_hashed
        )

        user = await self.user_repository.create(userDomain)

        return CreateUserResponseDto(
            id = user.id,
            document_number = user.document_number
        )