from typing import Optional

from sqlalchemy import String, select, BINARY
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.auth.utils.otp_manager import OTPManager
from app.auth.utils.phone_number import PhoneNumber
from app.core.database import Base


class UserBase(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String(36), primary_key=True)

    # Optional, т.к. во время регистрации у пользователя может не быть имени
    # Но это MVP момент, чтобы было меньше ручек =)
    # cached_phone: Mapped[Optional[str]] = mapped_column(String(20))
    name: Mapped[Optional[str]] = mapped_column(String(20))
    encrypted_phone: Mapped[bytes] = mapped_column(BINARY)

    def __repr__(self) -> str:
        return f"UserBase(id={self.id}, name={self.name}, encrypted_phone={self.encrypted_phone})"

    @staticmethod
    def update(new_object: 'UserBase', session):
        session.merge(new_object)

    def create(self, session):
        session.add(self)

    @classmethod
    def get_by_phone(cls, phone: PhoneNumber, session) -> 'UserBase':
        statement = select(UserBase).where(UserBase.encrypted_phone == OTPManager.encrypt_phone_number(phone))
        db_object = session.scalars(statement).one()
        return db_object
