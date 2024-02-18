from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer

from datetime import datetime, timedelta

from settings.jwt_settings import JWTSettings
from jose import JWTError, jwt


reusable_oauth2 = HTTPBearer(
    scheme_name='Authorization'
)


class JWT(JWTSettings):
    async def create_jwt_token(self, data: dict):
        to_encode = data.copy()

        if self.EXPIRE:
            expire = datetime.now() + + timedelta(self.EXPIRE)
        else:
            expire = datetime.now() + timedelta(minutes=15)

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.JWT_SECRET_KEY, algorithm=self.ALGORITHM)

        return encoded_jwt

    @classmethod
    async def get_current_user(cls, token=Depends(reusable_oauth2)) -> str:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token.credentials, cls.JWT_SECRET_KEY, algorithms=[cls.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise credentials_exception
            return username
        except JWTError:
            raise credentials_exception

    @classmethod
    def check_jwt_token(cls, func):
        async def wrapper(token: str, *args, **kwargs):
            try:
                jwt.decode(token, cls.JWT_SECRET_KEY, algorithms=[cls.ALGORITHM])
            except JWTError:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return await func(*args, **kwargs)

        return wrapper
