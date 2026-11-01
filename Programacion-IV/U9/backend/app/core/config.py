from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///foodstore_u9.db"
    SECRET_KEY: str = Field(min_length=32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, gt=0)
    COOKIE_SECURE: bool = False
    ADMIN_EMAIL: str = ""
    ADMIN_PASSWORD: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("SECRET_KEY")
    @classmethod
    def clave_configurada(cls, value: str) -> str:
        if value.startswith("REEMPLAZAR"):
            raise ValueError("Generar una SECRET_KEY propia en .env")
        return value


settings = Settings()
