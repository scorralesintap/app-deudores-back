from src.application.dtos.auth.login_dto import LoginDto
from src.application.dtos.users.create_user_dto import CreateUserDto
from src.application.dtos.auth.login_dto import LoginDto
from src.application.dtos.users.create_user_dto import CreateUserDto
from src.domain.ports.ports_in.i_register_user_use_case import IRegisterUserUseCase
from src.domain.ports.ports_in.i_login_use_case import ILoginUseCase


class UserServices:

    def __init__(
        self, 
        register_use_case: IRegisterUserUseCase,
        login_use_case: ILoginUseCase
    ):
        self.register_use_case = register_use_case
        self.login_use_case = login_use_case

    async def create(self, userDto: CreateUserDto): 
        return await self.register_use_case.create(userDto)
    
    async def login(self, loginDto: LoginDto):
        return await self.login_use_case.login(loginDto)