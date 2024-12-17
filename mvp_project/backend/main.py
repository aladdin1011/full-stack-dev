from fastapi import FastAPI, HTTPException
from pydantic import BaseModel,EmailStr,Field
from typing import List,Optional

app = FastAPI()

class HealthResponse(BaseModel):
    status: str
    message: str

@app.get("/health",response_model=HealthResponse)
async def health_check():
    return{"status": "OK","message":"Server is running and healthy!"}
# Локальное хранилище данных
users = [
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "role": "user"},
]

# Модель для валидации входных данных
class User(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    role: str = Field(..., pattern=r"^(admin|user)$")

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=50)
    email: Optional[EmailStr]
    role: Optional[str] = Field(None, pattern=r"^(admin|user)$")

# Функция для генерации уникального ID
def get_next_id():
    return max(user["id"] for user in users) + 1 if users else 1

@app.post("/users", response_model=dict)
def create_user(user: User):
    # Проверка уникальности email
    if any(existing_user["email"] == user.email for existing_user in users):
        raise HTTPException(status_code=400, detail="Email уже используется.")

    new_user = user.dict()
    new_user["id"] = get_next_id()
    users.append(new_user)
    return new_user

@app.get("/users", response_model=List[dict])
def get_users():
    return users

@app.get("/users/{id}", response_model=dict)
def get_user(id: int):
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")
    return user

@app.put("/users/{id}", response_model=dict)
def update_user(id: int, user_update: UserUpdate):
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    # Проверка уникальности email, если обновляется
    if user_update.email and any(existing_user["email"] == user_update.email for existing_user in users if existing_user["id"] != id):
        raise HTTPException(status_code=400, detail="Email уже используется.")

    # Обновление данных пользователя
    user.update(user_update.dict(exclude_unset=True))
    return user

@app.delete("/users/{id}", response_model=dict)
def delete_user(id: int):
    global users
    user = next((user for user in users if user["id"] == id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден.")

    users = [existing_user for existing_user in users if existing_user["id"] != id]
    return {"detail": "Пользователь удалён."}
