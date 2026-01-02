from src.application.dtos.auth.login_dto import LoginDto
from src.application.dtos.users.create_user_dto import CreateUserDto
from src.domain.ports.ports_in.auth import IRegisterUserUseCase
from src.domain.ports.ports_in.auth import ILoginUseCase


class UserServices:

    def __init__(
        self, 
        register_use_case: IRegisterUserUseCase,
        login_use_case: ILoginUseCase
    ):
        self.register_use_case = register_use_case
        self.login_use_case = login_use_case

    async def create(self, user_dto: CreateUserDto):
        return await self.register_use_case.create(user_dto)
    
    async def login(self, login_dto: LoginDto):
        return await self.login_use_case.login(login_dto)