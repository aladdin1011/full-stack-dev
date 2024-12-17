from fastapi import FastAPI
from pydantic import BaseModel ,EmailStr

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email : EmailStr
    role: str

@app.post("/users")
def create_user(user: User):
    return {"message": f"User {user.name} created successfully!"}