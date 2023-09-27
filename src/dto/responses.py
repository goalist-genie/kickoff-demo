from pydantic import BaseModel

class LoginResponseDto(BaseModel):
    access_token: str
    email: str
    full_name: str
    user_id: str