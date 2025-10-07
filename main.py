from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
import random
import time
import uuid
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Dobrodar API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


users_db = {}
otps = {}

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserRegister(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class EmailRequest(BaseModel):
    email: EmailStr

class OTPVerify(BaseModel):
    email: EmailStr
    code: str


@app.post("/auth/register")
async def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(400, "Пользователь уже зарегистрирован")
    
    
    user_id = str(uuid.uuid4())
    hashed_password = pwd_context.hash(user.password)
    
    users_db[user.email] = {
        "id": user_id,
        "email": user.email,
        "hashed_password": hashed_password,
        "is_active": True,
        "is_verified": False
    }
    
    return {
        "id": user_id,
        "email": user.email,
        "is_active": True,
        "message": "Пользователь зарегистрирован"
    }


@app.post("/auth/login")
async def login(user: UserLogin):
    db_user = users_db.get(user.email)
    
    if not db_user:
        raise HTTPException(400, "Пользователь не найден")
    
    if not pwd_context.verify(user.password, db_user["hashed_password"]):
        raise HTTPException(400, "Неверный пароль")
    
    
    token = f"token_{user.email}_{int(time.time())}"
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": db_user["id"],
        "email": user.email
    }

@app.post("/auth/email/request-code")
async def request_code(body: EmailRequest):
    code = str(random.randint(100_000, 999_999))
    otps[body.email] = {"code": code, "expires_at": time.time() + 300}
    
    
    print(f"📧 Send code {code} to {body.email}")
    
    return {"ok": True, "message": f"Код отправлен на {body.email}"}

@app.post("/auth/email/verify")
async def verify_code(body: OTPVerify):
    entry = otps.get(body.email)
    
    if not entry or entry["code"] != body.code:
        raise HTTPException(400, "Неверный код")
    
    if time.time() > entry["expires_at"]:
        raise HTTPException(400, "Код истёк")
    
   
    del otps[body.email]
    
 
    token = f"otp_token_{body.email}_{int(time.time())}"
    
    return {
        "ok": True,
        "message": "Вход успешен",
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/")
async def root():
    return {"message": "🚀 Dobrodar API запущен!"}

@app.get("/users/count")
async def users_count():
    return {"total_users": len(users_db)}

@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "users_registered": len(users_db),
        "active_otp_codes": len(otps)
    }

@app.get("/debug/users")
async def debug_users():
    return {"users": [{"email": email, "id": data["id"]} for email, data in users_db.items()]}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
