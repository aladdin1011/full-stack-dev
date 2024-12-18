from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field

app = FastAPI()

# Локальное хранилище пользователей
users = [
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "password": "password", "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "password": "paswword", "role": "user"},
]

# Модель для регистрации пользователя
class RegisterUser(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(default="user", regex="^(user|admin)$")

# Модель для входа пользователя
class LoginUser(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6)

@app.post("/auth/register")
def register_user(user: RegisterUser):
    # Проверить уникальность email
    if any(u["email"] == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already exists")

    # Создать нового пользователя
    new_user = {
        "id": len(users) + 1,
        "name": user.name,
        "email": user.email,
        "password": user.password,  # Пароль пока хранится как обычный текст
        "role": user.role,
    }
    users.append(new_user)
    return {"message": "User registered successfully", "user": new_user}

@app.post("/auth/login")
def login_user(credentials: LoginUser):
    # Найти пользователя по email
    user = next((u for u in users if u["email"] == credentials.email), None)
    if not user or user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    return {"message": f"Welcome, {user['name']}"}
