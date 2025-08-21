from pydantic import BaseModel
from typing import Optional, Dict, Any

class BaseUserModel(BaseModel):
    uid: str
    firebase_data: Dict[str, Any]   # decoded token (email, claims, etc.)
    
class UserModel(BaseUserModel):
    monthly_salary: Optional[float] = None
    hourly_pay: Optional[float] = None
    firestore_data: Optional[Dict[str, Any]] = None
    
class UserUpdateModel(BaseModel):
	monthly_salary: Optional[float] = None
	hourly_pay: Optional[float] = None