from pydantic import BaseModel, validator, ValidationError


class UserSchema(BaseModel):
    email: str
    lastname: str
    firstname: str
    email: str
    phone: str
    hashed_password: str

    @validator('hashed_password')
    def password(cls, value):
        if value == '2024':
            raise ValueError('Mot de passe invalide')
        return value

