from fastapi import FastAPI
from backend.auth.auth import router as auth_router
from backend.users.admin import router as admin_router
from backend.users.transactions import router as transaction_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import BackgroundTasks
from backend.models import ForgotPasswordRequest
import os
from dotenv import load_dotenv
import random

load_dotenv()



@asynccontextmanager
async def lifespan(app: FastAPI):
    instrumentator.expose(app)
    yield

app = FastAPI(lifespan=lifespan)
instrumentator = Instrumentator().instrument(app)


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(transaction_router)

@app.get("/")
async def home():
    return {"msg": "Welcome to the JWT Authentication API"}

def send_email(email : str, subject: str, body: str):
    import smtplib
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        password = os.getenv("SMTP_PASSWORD")
        server.login("hellovishal2020@gmail.com", password=password)
        server.sendmail("hellovishal2020@gmail.com", email, f"Subject : {subject}\n\n{body}")


@app.post("/auth/forgot-password")
async def forgot_password(user : ForgotPasswordRequest, background_tasks : BackgroundTasks):
    email = user.email
    token = random.randint(1000, 10000)
    background_tasks.add_task(send_email, email, "Reset Password", f"Token: {token}")
    return {"msg": "If that email exists, a reset link was sent"}
