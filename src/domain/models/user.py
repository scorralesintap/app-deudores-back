from dataclasses import dataclass
from datetime import datetime
from src.domain.value_objects.user.user_document_number import UserDocumentNumber
from src.domain.value_objects.user.user_password import UserPassword

@dataclass
class User:

    document_number: UserDocumentNumber
    password: UserPassword

    id: int | None = None
    is_active: bool = True
    failed_login_attempts: int = 0
    locked_until: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    last_login: datetime | None = None