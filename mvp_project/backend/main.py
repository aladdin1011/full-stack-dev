from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional

app = FastAPI()

# Модель для ответа на запрос /health
class HealthResponse(BaseModel):
    status: str
    message: str

# Эндпоинт для проверки состояния сервера
@app.get("/health", response_model=HealthResponse)
async def health_check():
    return {"status": "OK", "message": "Server is running and healthy!"}

# Локальное хранилище пользователей
users = [
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "role": "user"},
]

# Модель для валидации данных нового пользователя
class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    role: str = Field(..., pattern=r"^(admin|user)$")

# Модель для обновления данных пользователя
class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr]
    role: Optional[str] = Field(None, pattern=r"^(admin|user)$")

# Функция для генерации уникального ID для нового пользователя
def get_next_id():
    return max(user["id"] for user in users) + 1 if users else 1

# Эндпоинт для создания нового пользователя
@app.post("/users", response_model=dict)
def create_user(user: User):
    # Проверка уникальности email
    if any(existing_user["email"] == user.email for existing_user in users):
        raise HTTPException(status_code=400, detail="Email уже используется.")
    
    # Генерация нового ID и добавление пользователя в список
    new_user = user.dict()
    new_user["id"] = get_next_id()
    users.append(new_user)
    return new_user

# Эндпоинт для получения всех пользователей
@app.get("/users", response_model=List[dict])
def get_users():
    return users

# Эндпоинт для получения конкретного пользователя по ID
@app.get("/users/{id}", response_model=dict)
def get_user(id: int):
    # Поиск пользователя по ID
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    return user

# Эндпоинт для обновления данных пользователя по ID
@app.put("/users/{id}", response_model=dict)
def update_user(id: int, user_update: UserUpdate):
    # Поиск пользователя по ID
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    # Проверка уникальности email, если оно обновляется
    if user_update.email and any(existing_user["email"] == user_update.email for existing_user in users if existing_user["id"] != id):
        raise HTTPException(status_code=400, detail="Email уже используется.")

    # Обновление данных пользователя
    user.update(user_update.dict(exclude_unset=True))
    return user

# Эндпоинт для удаления пользователя по ID
@app.delete("/users/{id}", response_model=dict)
def delete_user(id: int):
    global users
    # Поиск пользователя по ID
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    # Удаление пользователя из списка
    users = [existing_user for existing_user in users if existing_user["id"] != id]
    return {"detail": "Пользователь удалён."}
