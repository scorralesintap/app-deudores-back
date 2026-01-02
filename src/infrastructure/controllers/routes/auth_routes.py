from fastapi import APIRouter, Depends, status

from src.infrastructure.services import JWTService
from src.application.dtos.auth.login_dto import LoginDto
from src.application.dtos.auth.login_reponse_dto import LoginResponseDto
from src.application.use_cases.auth.login_use_case import LoginUseCase
from src.application.use_cases.auth.register_user_use_case import RegisterUserUseCase
from src.infrastructure.adapters.user_repository_adapter import UserRepositoryAdapter
from src.infrastructure.database.connection import get_session
from src.application.dtos.users.create_user_dto import CreateUserDto
from src.application.dtos.users.create_user_response_dto import CreateUserResponseDto
from src.application.services.users.user_services import UserServices
from src.infrastructure.controllers.schemas.api_response_schema import ApiResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/auth", tags=["Auth"])

def get_services(session: AsyncSession = Depends(get_session)):
    repository = UserRepositoryAdapter(session)
    jwt_service = JWTService()
    register_use_case = RegisterUserUseCase(repository)
    login_use_case = LoginUseCase(repository, jwt_service)
    return UserServices(register_use_case, login_use_case)

@router.post("/register", response_model=ApiResponse[CreateUserResponseDto], status_code=status.HTTP_201_CREATED)
async def register(request: CreateUserDto, service: UserServices = Depends(get_services)):
    result = await service.create(request)
    return ApiResponse(
        status=True,
        data=result,
        message="Usuario registrado exitosamente"
    )

@router.post("/login", response_model=ApiResponse[LoginResponseDto])
async def login(request: LoginDto, service: UserServices = Depends(get_services)):
    result = await service.login(request)
    return ApiResponse(
        status=True,
        data=result,
        message="Inicio de sesión exitoso"
    )