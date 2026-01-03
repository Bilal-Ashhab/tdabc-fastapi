from pydantic import BaseModel


class DelayCreate(BaseModel):
    code: str
    minutes: int
    note: str | None = None
