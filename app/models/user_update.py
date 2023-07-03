from pydantic import BaseModel


class UserUpdate(BaseModel):
    name: str = None
    description: str = None
