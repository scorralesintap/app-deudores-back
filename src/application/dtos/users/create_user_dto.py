from pydantic import BaseModel, Field, field_validator

class CreateUserDto(BaseModel):
    document_number: str = Field(...)
    password: str = Field(...)