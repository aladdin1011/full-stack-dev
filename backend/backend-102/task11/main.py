from fastapi import FastAPI,Depends, HTTPException
from fastapi.security  import OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import BaseModel,EmailStr, Field
import bcrypt
from uuid import uuid4
from typing import List

app = FastAPI()

activate_refrseh_tokens = {}

ouath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Конфигурация для JWT
SECRET_KEY = "my_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7   

users = [
    {"id": 1, "name": "Adilet", "email": "adilet@example.com", "password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "role": "admin"},
    {"id": 2, "name": "Anuar", "email": "anuar@example.com", "password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "role": "user"},
    {"id": 3, "name": "Zhas", "email": "zhas@example.com", "password": bcrypt.hashpw("password".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'), "role": "admin"},
]

traveling = []

class RegisterUser(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    role: str = Field(default="user", pattern="^(user|admin)$")

class LoginUser(BaseModel):
    email: str
    password: str

class Travel(BaseModel):
    id: int
    name: str
    description: str
    date: datetime
    private: str = Field(default="public", pattern="^(public|private)$")    
    routes: List[str]

new_travel = Travel(
    id = 1,
    name="Trip to Almaty",
    description="Traveling to Almaty",
    date=datetime.now(),
    private="public",
    routes=[],
    
)

def create_access_token(data: dict):
    #Добавляем дату истечения токена 
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    # Генерируем токен
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(email: str):
    token_id = str(uuid4())
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {"sub": email, "token_id": token_id, "exp": expire}
    refresh_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    # Сохраняем токен как активный
    activate_refrseh_tokens[token_id] = {"email" : email, "expires_at": expire}
    return refresh_token

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Возвращаем данные токена, если он валиден
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

def check_user_role(token_data: dict, required_role: str):
    user_role = token_data.get("role")
    if user_role != required_role:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied: requires {required_role} role"
        )

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
def login_user(email: str, password: str):
    # Проверям пользователя
    user = next((u for u in users if u["email"] == email), None)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        return {"error": "Invalid email or password"}

    # Удаляем все активные Refresh Token для данного пользователя
    token_to_revoke = [key for key, value in activate_refrseh_tokens.items() if value["email"] == email]
    for token_id in token_to_revoke:
        del activate_refrseh_tokens[token_id]

    # Генерируем Access Token и Refresh Token
    access_token = create_access_token({"sub": user["email"],"role": user["role"], "name": user["name"]})
    refresh_token = create_refresh_token(user["email"])

    return { 
        "access_token": access_token,
        "refresh_token": refresh_token
    }

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

def check_user_role(token_data: dict, required_role: str):
    user_role = token_data.get("role")
    if user_role != required_role:
        raise HTTPException(
            status_code=403,
            detail=f"Access denied: requires {required_role} role"
        )

@app.get("/admin")
def admin_route(token: str = Depends(ouath2_scheme)):
    user_data = verify_access_token(token)
    check_user_role(user_data, "admin")
    return {"message": "Welcome, Admin! You have full access"}

@app.get("/user-resource")
def user_resource(token: str = Depends(ouath2_scheme)):
    user_data = verify_access_token(token)
    check_user_role(user_data,"user")
    return {"message": f"Welcome, {user_data["name"]}! This resource if for users only."}

@app.get("/auth/refresh")
def refresh_access_token(refresh_token: str):
    try:
        # Проверяем валидность Refresh Token
        payload = jwt.decode(refresh_token, SECRET_KEY , algorithms=[ALGORITHM])
        token_id = payload.get("token_id")
        email = payload.get("sub")

        # Проверяем, что токен активен
        if token_id not in activate_refrseh_tokens:
            raise HTTPException(status_code=401, detail="Refresh token is not active")

        # Удаляем старый токен из списка активных
        del activate_refrseh_tokens[token_id]

        #  Генерируем новый Access Token и Refresh Token
        new_access_token = create_access_token({"sub": email})
        new_refresh_token = create_refresh_token(email)

        return {
            "access_token": new_access_token,
            "refresh_token": new_refresh_token
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
    
@app.post("/auth/logout")
def logout_user(token: str= Depends(ouath2_scheme)):
    # Проверяем токен
    payload = verify_access_token(token)
    email = payload.get("sub")

    # Удаляем все активные Refresh Token для данного пользователя
    token_to_revoke = [key for key, value in activate_refrseh_tokens.items() if value["email"] == email]
    for token_id in token_to_revoke:
        del activate_refrseh_tokens[token_id]
    
    return {"message" : "Successfully logged out"}

@app.post("/travels")
def post_travel(travel: Travel, token: str = Depends(ouath2_scheme)):
    user_data = verify_access_token(token)
    new_travel = {
        "id": len(traveling) + 1,
        "name": travel.name, #owner
        "description": travel.description,
        "date": travel.date,
        "private": travel.private,
        "routes": travel.routes,
        "owner": user_data["sub"]  #Привязка пользователя
    }
    traveling.append(new_travel)
    return {"message": "Travel added successfully", "travel": new_travel}

@app.get("/travels")
def get_user_travels(token: str = Depends(ouath2_scheme)):
    user_data = verify_access_token(token)

    user_travel =[p for p in traveling if p["owner"] == user_data["sub"]]
    
    return {"travels": user_travel}

@app.get("/travels/{travel_id}")
def get_travel_id(travel_id: int, token: str = Depends(ouath2_scheme)):
    user_data = verify_access_token(token)

    user_travel =[p for p in traveling if p["owner"] == user_data["sub"] and p["id"] == travel_id]
    if not user_travel:
        raise HTTPException(status_code=404, detail="Travel not found")
    
    return {"travel": user_travel}    


@app.put("/travels/{travel_id}")
def update_travel(travel_id: int, travel: Travel, token: str = Depends(ouath2_scheme)):
    user_data = verify_access_token(token)
    my_travel = next((t for t in traveling if t["id"] == travel_id), None)
    if not my_travel:
        raise HTTPException(status_code=404, detail="Travel not found or not authorized")
    
    my_travel.update(travel.dict())
    return{"message": "Travel updated successfully", "travel": my_travel}
    