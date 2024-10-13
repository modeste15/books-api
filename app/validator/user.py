from pydantic import BaseModel, validator, ValidationError,EmailStr
import re

class UserSchema(BaseModel):
    lastname: str
    firstname: str
    email: EmailStr
    phone: str
    password: str
    image : str

    @validator('password')
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError('Le mot de passe doit comporter au moins 8 caractères.')
        if not re.search("[a-z]", value):
            raise ValueError('Le mot de passe doit contenir au moins une lettre minuscule.')
        if not re.search("[A-Z]", value):
            raise ValueError('Le mot de passe doit contenir au moins une lettre majuscule.')
        if not re.search("[0-9]", value):
            raise ValueError('Le mot de passe doit contenir au moins un chiffre.')
        if not re.search("[@#$%^&+=]", value):
            raise ValueError('Le mot de passe doit contenir au moins un caractère spécial (@, #, $, %, etc.).')
        if all(char == value[0] for char in value):
            raise ValueError('Le mot de passe ne doit pas contenir des caractères identiques en séquence.')
        return value

    @validator('phone')
    def validate_phone(cls, value):
        if not re.match(r'^\+?\d{9,15}$', value):
            raise ValueError('Numéro de téléphone invalide. Il doit contenir entre 9 et 15 chiffres.')
        return value

