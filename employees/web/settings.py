import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    db_server: str = os.getenv('DB_SERVER', '127.0.0.1')
    db_name: str = os.getenv('DB_NAME', 'TestDB')
    db_username: str = os.getenv('DB_USERNAME', 'SA')
    db_password: str = os.getenv('DB_PASSWORD', 'Mypassword123*')

    jwt_secret: str = os.getenv('JWT_SECRET', 'mysecret')
