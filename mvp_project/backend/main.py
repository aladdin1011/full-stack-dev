from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class HealthResponse(BaseModel):
    status: str
    message: str

@app.get("/health",response_model=HealthResponse)
async def health_check():
    return{"status": "OK","message":"Server is running and healthy!"}