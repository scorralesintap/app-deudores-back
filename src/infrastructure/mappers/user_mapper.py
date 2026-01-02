from src.domain.value_objects.user.user_document_number import UserDocumentNumber
from src.domain.models.user import User as DomainUser
from src.infrastructure.database.entities.user import User as UserEntity
from src.domain.value_objects.user.user_password import UserPassword

class UserMapper:

    @staticmethod
    def to_domain(entity: UserEntity) -> DomainUser:
        return DomainUser(
            id=entity.id,
            document_number=UserDocumentNumber(entity.document_number),
            password=UserPassword(entity.password_hash, already_hashed=True),
            is_active=entity.is_active,
            failed_login_attempts=entity.failed_login_attempts,
            locked_until=entity.locked_until,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            last_login=entity.last_login,
        )

    @staticmethod
    def to_entity(domain: DomainUser) -> UserEntity:
        entity = UserEntity(
            document_number=domain.document_number.value,
            password_hash=domain.password.value,
            is_active=domain.is_active,
            failed_login_attempts=domain.failed_login_attempts,
            locked_until=domain.locked_until,
            created_at=domain.created_at,
            updated_at=domain.updated_at,
            last_login=domain.last_login,
        )
        if domain.id is not None:
            entity.id = domain.id
        return entity

