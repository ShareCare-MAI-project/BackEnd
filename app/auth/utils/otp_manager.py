from passlib.context import CryptContext

from app.auth.utils.phone_number import PhoneNumber


class OTPManager:
    _crypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    _otp_requests = {}  # TODO: придумать, как их чистить =)

    @classmethod
    def verify(cls, phone_number: PhoneNumber, code: str) -> bool:
        return cls._otp_requests[cls._hash_phone_number(phone_number)] == cls._hash_opt(code)

    @classmethod
    def add_otp_request(cls, phone_number: PhoneNumber, code: str):
        cls._otp_requests[cls._hash_phone_number(phone_number)] = cls._hash_opt(code)

    @classmethod
    def _hash_opt(cls, opt: str):
        return cls._crypt_context.hash(opt)

    @classmethod
    def _hash_phone_number(cls, phone_number: PhoneNumber):
        return cls._crypt_context.hash(phone_number)
