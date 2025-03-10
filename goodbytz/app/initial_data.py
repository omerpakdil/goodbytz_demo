import logging

from sqlalchemy.orm import Session

from app import crud, schemas
from app.db.session import SessionLocal
from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init_db(db: Session) -> None:
    user = crud.user.get_by_email(db, email="admin@goodbytz.com")
    if not user:
        user_in = schemas.UserCreate(
            email="admin@goodbytz.com",
            password="admin123",
            full_name="Admin",
            is_superuser=True,
            is_kitchen_staff=True,
        )
        user = crud.user.create(db, obj_in=user_in)
        logger.info("Admin kullanıcısı oluşturuldu")
    
    kitchen_user = crud.user.get_by_email(db, email="kitchen@goodbytz.com")
    if not kitchen_user:
        user_in = schemas.UserCreate(
            email="kitchen@goodbytz.com",
            password="kitchen123",
            full_name="Mutfak Personeli",
            is_superuser=False,
            is_kitchen_staff=True,
        )
        kitchen_user = crud.user.create(db, obj_in=user_in)
        logger.info("Mutfak personeli kullanıcısı oluşturuldu")
    
    # Normal kullanıcı oluştur
    normal_user = crud.user.get_by_email(db, email="user@goodbytz.com")
    if not normal_user:
        user_in = schemas.UserCreate(
            email="user@goodbytz.com",
            password="user123",
            full_name="Test Kullanıcı",
            is_superuser=False,
            is_kitchen_staff=False,
        )
        normal_user = crud.user.create(db, obj_in=user_in)
        logger.info("Normal kullanıcı oluşturuldu")


def main() -> None:
    logger.info("Veritabanı başlatılıyor")
    db = SessionLocal()
    init_db(db)
    logger.info("Veritabanı başlatma tamamlandı")


if __name__ == "__main__":
    main() 