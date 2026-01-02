import re
from argon2 import PasswordHasher

class UserPassword:
    def __init__(self, password: str, already_hashed: bool = False):
        if already_hashed:
            self._hashed_password = password
        else:
            self._validate(password)
            self._hashed_password = self._hash(password)

    def _validate(self, password: str):
        if not password or password.strip() == "":
            raise ValueError("La contraseña es obligatoria")

        if len(password) < 8:
            raise ValueError("La contraseña debe tener mínimo 8 caracteres")

        if not re.search(r"[A-Za-z]", password):
            raise ValueError("La contraseña debe contener al menos una letra")

        if not re.search(r"[0-9]", password):
            raise ValueError("La contraseña debe contener al menos un número")

    def _hash(self, password: str) -> str:
        ph = PasswordHasher()
        return ph.hash(password)

    def verify(self, plain_password: str) -> bool:
        from argon2.exceptions import VerifyMismatchError
        ph = PasswordHasher()
        try:
            ph.verify(self._hashed_password, plain_password)
            return True
        except VerifyMismatchError:
            return False

    @property
    def value(self) -> str:
        return self._hashed_password

    def __eq__(self, other):
        return isinstance(other, UserPassword) and self._hashed_password == other._hashed_password

    def __str__(self):
        return self._hashed_password