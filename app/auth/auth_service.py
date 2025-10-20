import uuid

from fastapi import HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from app.auth.auth_models import LoginRequest, OTPVerifyRequest, AuthResponse
from app.auth.user_base import UserBase
from app.auth.utils.otp_manager import OTPManager
from app.core.database import default_db_request

FAKE_OTP = "1111"


class AuthService:

    @staticmethod
    async def request_otp(request: LoginRequest) -> dict:
        """Отправить OTP код на телефон"""
        phone = request.phone

        code = FAKE_OTP

        OTPManager.add_otp_request(phone, code)

        return {"success": True}

    @staticmethod
    async def verify_otp(request: OTPVerifyRequest) -> AuthResponse:
        """Если код совпадает, проводим авторизацию"""
        phone = request.phone
        otp = request.otp
        if not OTPManager.verify(phone_number=phone, code=otp):
            raise HTTPException(
                status_code=HTTP_400_BAD_REQUEST,
                detail="Неверный или просроченный код подтверждения"
            )

        user: UserBase = default_db_request(lambda session: UserBase.get_by_phone(phone, session=session))
        username = user.name if user is not None else None
        token = str(uuid.uuid4())

        return AuthResponse(
            token=token,
            name=username
        )
