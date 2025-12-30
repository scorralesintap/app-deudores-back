from pydantic import BaseModel, Field, field_validator

class CreateUserDto(BaseModel):
    document_number: str
    password: str

    @field_validator('document_number')
    @classmethod
    def validate_document_number(cls, value):
        if not value or not value.strip():
            raise ValueError("El número de documento es requerido")
        if len(value) < 6:
            raise ValueError("El número documento debe tener mínimo 6 caracteres")
        if len(value) > 20:
            raise ValueError("El número documento debe tener máximo 20 caracteres")
        return value
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if not value or not value.strip():
            raise ValueError("La contraseña es requerida")
        return value

