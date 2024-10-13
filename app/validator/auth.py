from pydantic import BaseModel, validator, ValidationError,EmailStr


class AuthSchema(BaseModel):
    email: EmailStr
    password: str



