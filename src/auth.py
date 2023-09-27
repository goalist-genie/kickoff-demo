import jwt
from dto.objects import User
from exceptions import UnauthorizedException
from datetime import datetime, timedelta
from config import settings
from stores import user_store


def _find_user_by_email(email: str) -> User:
    for user in user_store:
        if user.email == email:
            return user

    raise UnauthorizedException("Could not validate credentials")

def create_access_token(user: User):
    expiry = datetime.utcnow() + timedelta(days=1)
    encode = {
        "id": user.id,
        "sub": user.email,
        "email": user.email,
        "name": user.full_name,
        "exp": expiry,
    }
    
    return jwt.encode(encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def verify_token(token: str) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return _find_user_by_email(payload["email"])
    except jwt.PyJWTError:
        raise UnauthorizedException("Could not validate credentials")
