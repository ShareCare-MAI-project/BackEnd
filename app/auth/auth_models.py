from typing import Optional
from pydantic import BaseModel, Field, UUID7
from app.auth.utils.phone_number import PhoneNumber


class LoginRequest(BaseModel):
    phone: PhoneNumber  # Кастомный класс, интегрированный с pydantic


# OTP = OneTimePassword
class OTPVerifyRequest(BaseModel):
    phone: PhoneNumber  # Кастомный класс, интегрированный с pydantic
    otp: str = Field(min_length=4, max_length=4, examples=["1234", "4421"], description="OTP Код")


class AuthResponse(BaseModel):
    token: UUID7 = Field(description="UUID7 токен")  # str(uuid)
    # Если имени нет, то перебрасываем на заполнение профиля (в приложении)
    name: Optional[str] = Field(None,
                                description="Имя пользователя, если заполнено, Иначе -> отправляем заполнять в "
                                            "приложении")
