from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kimlik doğrulanamadı",
        )
    user = db.query(models.User).filter(models.User.id == token_data.sub).first()
    if not user:
        raise HTTPException(status_code=404, detail="Kullanıcı bulunamadı")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Kullanıcı aktif değil")
    return user


def get_current_active_superuser(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="Kullanıcının yeterli yetkisi yok"
        )
    return current_user


def get_current_kitchen_staff(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not current_user.is_kitchen_staff and not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="Kullanıcının mutfak personeli yetkisi yok"
        )
    return current_user 