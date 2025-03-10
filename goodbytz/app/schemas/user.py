from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


# Ortak özellikler
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    is_kitchen_staff: bool = False
    full_name: Optional[str] = None


# Oluşturma sırasında kullanılacak özellikler
class UserCreate(UserBase):
    email: EmailStr
    password: str


# Güncelleme sırasında kullanılacak özellikler
class UserUpdate(UserBase):
    password: Optional[str] = None


# Veritabanından okuma sırasında kullanılacak özellikler
class UserInDBBase(UserBase):
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


# API'den döndürülecek kullanıcı
class User(UserInDBBase):
    pass


# Veritabanında saklanan ek veriler
class UserInDB(UserInDBBase):
    hashed_password: str 