from fastapi import APIRouter, Header, HTTPException
from app.services.firebase_service import verify_token, get_user_data

router = APIRouter()

@router.get("/me")
def get_profile(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    
    try:
        token = authorization.split(" ")[1]  # Expect "Bearer <token>"
        decoded = verify_token(token)
        user_data = get_user_data(decoded["uid"])
        return {"uid": decoded["uid"], "firebase_data": decoded, "firestore_data": user_data}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
