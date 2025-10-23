from cryptography.fernet import Fernet
from passlib.context import CryptContext
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app.auth.utils.phone_number import PhoneNumber
from app.core.config import FERNET_KEY


class OTPManager:
    _fernet = Fernet(FERNET_KEY)
    _otp_requests = {}  # TODO: придумать, как их чистить =)

    @classmethod
    def verify(cls, phone_number: PhoneNumber, code: str) -> bool:
        encrypted_phone_number = cls.encrypt_phone_number(phone_number)
        return ((encrypted_phone_number in cls._otp_requests) and
                cls._otp_requests[encrypted_phone_number] == cls._encrypt_opt(code))

    @classmethod
    def add_otp_request(cls, phone_number: PhoneNumber, code: str):
        cls._otp_requests[cls.encrypt_phone_number(phone_number)] = cls._encrypt_opt(code)

    @classmethod
    def _encrypt_opt(cls, opt: str) -> bytes:
        return cls._fernet.encrypt(opt.encode())

    @classmethod
    def encrypt_phone_number(cls, phone_number: PhoneNumber) -> bytes:
        return cls._fernet.encrypt(phone_number.encode())

    @classmethod
    def _decrypt_opt(cls, encrypted_opt: bytes) -> str:
        return cls._fernet.decrypt(encrypted_opt).decode()

    @classmethod
    def decrypt_phone_number(cls, encrypted_phone_number: bytes) -> str:
        return cls._fernet.decrypt(encrypted_phone_number).decode()
