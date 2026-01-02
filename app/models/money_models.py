from pydantic import BaseModel

class MoneyInput(BaseModel):
    price: float  # Input float

class MoneyOutput(BaseModel):
    price: float
    working_hours: int
