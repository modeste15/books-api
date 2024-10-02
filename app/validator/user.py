from pydantic import BaseModel, validator, ValidationError,EmailStr


class UserSchema(BaseModel):
    lastname: str
    firstname: str
    email: EmailStr
    phone: str
    password: str
    image : str

    @validator('password')
    def password(cls, value):
        if all(char == value[0] for char in value) : 
            raise ValueError('Mot de passe invalide')
        return value

