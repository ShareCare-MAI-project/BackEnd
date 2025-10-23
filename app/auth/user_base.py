from typing import Optional

from sqlalchemy import String, select, LargeBinary, Integer
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from app.auth.utils.otp_manager import OTPManager
from app.auth.utils.phone_number import PhoneNumber
from app.core.database import Base


class UserBase(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Optional, т.к. во время регистрации у пользователя может не быть имени
    # Но это MVP момент, чтобы было меньше ручек =)
    # cached_phone: Mapped[Optional[str]] = mapped_column(String(20))
    name: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    encrypted_phone: Mapped[bytes] = mapped_column(LargeBinary)

    def __repr__(self) -> str:
        return f"UserBase(id={self.id}, name={self.name}, encrypted_phone={self.encrypted_phone})"

    @staticmethod
    async def update(new_object: 'UserBase', session):
        session.merge(new_object)

    async def create(self, session):
        session.add(self)

    @classmethod
    async def get_by_phone(cls, phone: PhoneNumber, session) -> 'UserBase':
        """
        :param phone:
        :param session:
        :return: МОЖЕТ ВЕРНУТЬ None!!! (не могу указать, т.к. питон...)
        """
        statement = select(UserBase).where(UserBase.encrypted_phone == OTPManager.encrypt_phone_number(phone))
        return (await session.scalars(statement)).one_or_none()
