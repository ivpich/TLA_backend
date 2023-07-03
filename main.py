from fastapi import FastAPI
from app.core.middleware import TelegramAuthMiddleware
from fastapi import FastAPI
from app.api.v1 import auth, user

app = FastAPI()

app.add_middleware(TelegramAuthMiddleware)

app = FastAPI()

app.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/v1/user", tags=["User"])
