from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
import bcrypt
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Конфигурация для JWT
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

users = [
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "role": "user"},
    {"id": 3, "name": "Zhas", "email": "zhas@example.com", "password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "role": "user"},
]

class RegisterUser(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(default="user", pattern="^(user|admin)$")

class LoginUser(BaseModel):
    email: str
    password: str

def create_access_token(data: dict):
    #Добавляем дату истечения токена 
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    # Генерируем токен
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post("/auth/register")
def register_user(user: RegisterUser):
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already exists")
    
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "role": user.role,
    }
    users.append(new_user)
    return {"message": "User registered successfully", "user": new_user}


@app.post("/auth/login")
def login_user(user: LoginUser):
    # Проверяем пользователя
    user_data = next((u for u in users if u["email"] == user.email), None)
    if not user_data or not bcrypt.checkpw(user.password.encode("utf-8"), user_data["password"].encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Создаем токен с информацией
    token = create_access_token({"sub": user_data["email"], "role": user_data["role"], "name": user_data["name"]})
    return {"access_token": token}

# Проверка токена
def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.get("/protected")
def protected_route(token: str = Depends(ouath2_scheme)):
     # Проверяем токен
    user_data = verify_access_token(token)
    return {"message": f"Welcome, your role is {user_data['role']}"}

@app.get("/me")
def get_current_user(token: str = Depends(ouath2_scheme)):
    user_data = verify_access_token(token)
    return {
        "email": user_data["sub"],
        "name": user_data["name"],
        "role": user_data["role"]
    }
