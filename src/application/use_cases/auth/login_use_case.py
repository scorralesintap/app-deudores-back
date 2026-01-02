from datetime import datetime, timedelta, timezone

from src.infrastructure.services.datetime_service import DatetimeService
from src.domain.ports.ports_out.services import IJWTService
from src.application.dtos.auth.login_dto import LoginDto
from src.application.dtos.auth.login_reponse_dto import LoginResponseDto
from src.domain.ports.ports_in.auth import ILoginUseCase
from src.domain.ports.ports_out.repositories import IUserRepository

MAX_LOGIN_ATTEMPTS = 5
LOCK_DURATION_HOURS = 24

class LoginUseCase(ILoginUseCase):
    def __init__(self, user_repository: IUserRepository, jwt_service: IJWTService):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def login(self, login_dto: LoginDto) -> LoginResponseDto:
        user = await self.user_repository.get_by_document_number(login_dto.document_number)

        if not user:
            raise Exception("Credenciales inválidas")

        if not user.is_active:
            raise Exception("Usuario inactivo")

        if user.locked_until and user.locked_until > datetime.now(timezone.utc):
            raise Exception(f"La cuenta está bloqueada hasta { DatetimeService.format_datetime(user.locked_until) }")

        if user.locked_until and user.locked_until <= datetime.now(timezone.utc):
            await self.user_repository.update_failed_attempts(user, 0, None)

        if not user.password.verify(login_dto.password):
            attempts = user.failed_login_attempts + 1
            locked_until = None

            if attempts >= MAX_LOGIN_ATTEMPTS:
                locked_until = datetime.now(timezone.utc) + timedelta(hours=LOCK_DURATION_HOURS)

            await self.user_repository.update_failed_attempts(user, attempts, locked_until)

            if locked_until:
                raise Exception(f"Cuenta bloqueada por {LOCK_DURATION_HOURS} horas debido a múltiples intentos fallidos")

            raise Exception("Credenciales inválidas")
        
        await self.user_repository.update_last_login(user)
        
        access_token = self.jwt_service.create_access_token(
            data = {
                "sub": user.document_number.value,
                "user_id": user.id,
            })

        return LoginResponseDto(
            access_token = access_token,
            token_type = "bearer"
        )