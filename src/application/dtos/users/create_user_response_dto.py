from pydantic import BaseModel

class CreateUserResponseDto(BaseModel):
    id: int
    document_number: str