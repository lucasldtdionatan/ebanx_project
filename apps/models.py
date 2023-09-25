from pydantic import BaseModel


class EventData(BaseModel):
    type: str
    destination: str | None = None
    amount: float
    origin: str | None = None