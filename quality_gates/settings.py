from pydantic_settings import BaseSettings
from pydantic import SecretStr


class Settings(BaseSettings):
    """
    Config for application
    """
    db_dsn: str
    host: str = '0.0.0.0'
    port: int = 8000
    api_token: SecretStr
    swagger: bool = True
    debug: bool = False
    jira_host: str
    jira_token: SecretStr
    swagger: bool = False

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
