import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, EmailStr, PostgresDsn, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 dakika * 24 saat * 8 gün = 8 gün
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    # BACKEND_CORS_ORIGINS, bir string listesi olarak tanımlanır
    # örn: ["http://localhost", "http://localhost:4200", "http://localhost:3000"]
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "GoodBytz"
    
    # PostgreSQL
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "goodbytz"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )
    
    # MQTT Ayarları
    MQTT_BROKER_HOST: str = "localhost"
    MQTT_BROKER_PORT: int = 1883
    MQTT_CLIENT_ID: str = "goodbytz_backend"
    MQTT_USERNAME: Optional[str] = None
    MQTT_PASSWORD: Optional[str] = None
    
    # Email Ayarları
    SMTP_TLS: bool = True
    SMTP_PORT: Optional[int] = None
    SMTP_HOST: Optional[str] = None
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    EMAILS_FROM_NAME: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings() 