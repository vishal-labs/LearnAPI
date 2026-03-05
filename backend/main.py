from fastapi import FastAPI
from backend.auth.auth import router as auth_router
from backend.users.admin import router as admin_router
from backend.users.transactions import router as transaction_router
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from prometheus_fastapi_instrumentator import Instrumentator





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
