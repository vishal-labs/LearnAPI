from fastapi import FastAPI
from backend.auth.auth import router as auth_router
from backend.users.admin import router as admin_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(admin_router)

@app.get("/")
async def home():
    return {"msg": "Welcome to the JWT Authentication API"}
