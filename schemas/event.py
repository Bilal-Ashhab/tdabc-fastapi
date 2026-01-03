from pydantic import BaseModel


class EventCreate(BaseModel):
    event_type: str
    actor_role: str = "nurse"
