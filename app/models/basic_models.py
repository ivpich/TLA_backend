from pydantic import BaseModel


class InitData(BaseModel):
    telegram_data: str
