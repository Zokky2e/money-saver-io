from fastapi import Header, HTTPException, Depends
from app.models.user_models import UserModel
from app.services.firebase_service import get_user_data, verify_token

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    try:
        token = authorization.split(" ")[1]
        decoded = verify_token(token)
        return decoded  # contains uid, email, etc.
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Unauthorized: {e}")


def get_current_user_data(user):
    uid = user["uid"]  # from verified token
    user_data = get_user_data(uid)

    return UserModel(
        uid=uid,
        firebase_data=user,
        monthly_salary=user_data.get("monthly_salary"),
        hourly_pay=user_data.get("hourly_pay"),
        firestore_data=user_data
    )