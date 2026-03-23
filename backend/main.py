from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from backend.auth.auth import router as auth_router
from backend.users.admin import router as admin_router
from backend.users.transactions import router as transaction_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator
from fastapi import BackgroundTasks
from backend.models import ForgotPasswordRequest
from backend.config import settings
from backend.auth.validate import createPasswordResetToken
import random
import jwt



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

@app.exception_handler(jwt.ExpiredSignatureError)
async def expired_signature_handler(request: Request, exc: jwt.ExpiredSignatureError):
    return JSONResponse(status_code=401, content={"detail": "Session Expired, Login Again"})

@app.exception_handler(jwt.InvalidTokenError)
async def invalid_token_handler(request: Request, exc: jwt.InvalidTokenError):
    return JSONResponse(status_code=401, content={"detail": "Invalid User authentication"})

@app.get("/")
async def home():
    return {"msg": "Welcome to the JWT Authentication API"}

def send_email(email : str, subject: str, body: str):
    import smtplib
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        password = settings.SMTP_PASSWORD
        server.login("hellovishal2020@gmail.com", password=password)
        server.sendmail("hellovishal2020@gmail.com", email, f"Subject : {subject}\n\n{body}")


@app.post("/auth/forgot-password")
async def forgot_password(user : ForgotPasswordRequest, background_tasks : BackgroundTasks):
    email = user.email
    token = createPasswordResetToken(email)
    reset_link = f"http://localhost:8080/reset-password?token={token}"
    background_tasks.add_task(send_email, email, "Reset Password", f"Click here to reset: {reset_link}\nOr use token: {token}")
    return {"msg": "If that email exists, a reset link was sent"}
