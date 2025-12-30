from pydantic import BaseModel, Field, field_validator

class LoginDto(BaseModel):
    document_number: str
    password: str

    @field_validator('document_number')
    @classmethod
    def validate_document_number(cls, value):
        if not value or not value.strip():
            raise ValueError("El número de documento es requerido")
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if not value or not value.strip():
            raise ValueError("La contraseña es requerida")
        return value