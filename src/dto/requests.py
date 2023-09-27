from pydantic import BaseModel, EmailStr, validator
from exceptions import BadRequestException
from utils import is_email_unique


class CreateUserDto(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    password2: str
    
    @validator('password2')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise BadRequestException('passwords do not match')
        return v
    
    @validator("email")
    def email_must_be_unique(cls, v, values, **kwargs):
        if not is_email_unique(v):
            raise BadRequestException("Email already exists")
        return v
    
class LoginDto(BaseModel):
    email: EmailStr
    password: str