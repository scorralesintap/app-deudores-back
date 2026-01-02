from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Optional

class IJWTService(ABC):

    @abstractmethod
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None) -> str:
        pass

    @abstractmethod
    def verify_token(self, token: str) -> dict | None:
        pass

    @abstractmethod
    def decode_access_token(self, token: str) -> Optional[dict]:
        pass