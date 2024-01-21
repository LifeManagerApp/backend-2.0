import os


class JWTSettings:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    EXPIRE = int(os.getenv("EXPIRE"))
    ALGORITHM = os.getenv("ALGORITHM")
