from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.ports.ports_out.i_user_repository import IUserRepository
from src.domain.models.user import User as DomainUser
from src.infrastructure.database.entities.user import User as UserEntity
from src.infrastructure.mappers.user_mapper import UserMapper
from src.domain.value_objects.user.user_password import UserPassword

class UserRepositoryAdapter(IUserRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_document_number(self, document_number: str) -> DomainUser | None:
        query = select(UserEntity).where(UserEntity.document_number == document_number)
        result = await self.session.execute(query)
        entity = result.scalar_one_or_none()

        if entity is None:
            return None

        return UserMapper.to_domain(entity)

    async def create(self, user: DomainUser) -> DomainUser:
        entity = UserEntity(
            document_number = user.document_number.value,
            password_hash = user.password.value,
        )
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)

        return UserMapper.to_domain(entity)

    async def update_failed_attempts(self, user: DomainUser, attempts: int,
                                     locked_until: datetime | None = None) -> None:
        query = select(UserEntity).where(UserEntity.id == user.id)
        result = await self.session.execute(query)
        entity = result.scalar_one_or_none()

        if entity is None:
            return None

        entity.failed_login_attempts = attempts
        entity.locked_until = locked_until
        entity.updated_at = datetime.now(timezone.utc)

        await self.session.commit()
        return None

    async def update_last_login(self, user: DomainUser) -> None:
        query = select(UserEntity).where(UserEntity.id == user.id)
        result = await self.session.execute(query)
        entity = result.scalar_one()

        entity.last_login = datetime.now(timezone.utc)
        entity.failed_login_attempts = 0
        entity.locked_until = None
        entity.updated_at = datetime.now(timezone.utc)