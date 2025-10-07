from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import random, time
app = FastAPI(title="Email OTP API")


otps: dict[str, dict] = {}

class EmailRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    code: str

@app.post("/auth/email/request-code")
async def request_code(body: EmailRequest):
    code = str(random.randint(100_000, 999_999))
    otps[body.email] = {"code": code, "expires_at": time.time() + 300}

    # TODO: Send a real email here. For demo:
    print(f"Send code {code} to {body.email}")

    return {"ok": True}

@app.post("/auth/email/verify")
async def verify_code(body: OTPVerify):
    entry = otps.get(body.email)
    if not entry or entry["code"] != body.code:
        raise HTTPException(400, "Неверный код")
    if time.time() > entry["expires_at"]:
        raise HTTPException(400, "Код истёк")
    del otps[body.email]
    return {"ok": True}