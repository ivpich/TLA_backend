from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from .telegram_verification import verify_telegram_data


class TelegramAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method.lower() == "post":
            form_data = await request.form()
            telegram_data = form_data.get('initData', '')  # assuming initData is a field in the form data

            if not verify_telegram_data(telegram_data):
                return JSONResponse(status_code=401, content={"detail": "Invalid user"})

        response = await call_next(request)
        return response
