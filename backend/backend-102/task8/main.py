from fastapi import FastAPI,Depends, HTTPException
from fastapi.security  import OAuth2PasswordBearer
from datetime import datetime,timedelta
from jose import jwt, JWTError, ExpiredSignatureError
from pydantic import BaseModel,EmailStr, Field
import bcrypt

app = FastAPI()


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

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


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
def login_user(user: LoginUser):
    # Проверяем пользователя
    user_data = next((u for u in users if u["email"] == user.email), None)
    if not user_data or not bcrypt.checkpw(user.password.encode("utf-8"), user_data["password"].encode("utf-8")):
        return {"error": "Invalid email or password"}

    # Создаем токен с информацией
    access_token = create_access_token({"sub": user_data["email"], "role": user_data["role"], "name": user_data["name"]})
    refresh_token = create_refresh_token({"sub": user_data["email"]})
    
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
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401,detail="Invalid token")
        
        #Генерируем новый Access Token
        new_access_token = create_access_token({"sub": email})
        return {"access_token" : new_access_token}

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
