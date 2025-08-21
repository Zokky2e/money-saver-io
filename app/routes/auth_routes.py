from fastapi import APIRouter, Depends
from app.models.user_models import UserModel, UserUpdateModel
from app.services.firebase_service import get_user_data, update_user_data
from app.dependencies import get_current_user, get_current_user_data

router = APIRouter()

@router.get("/me")
def get_profile(user=Depends(get_current_user)):
    return get_current_user_data(user)

@router.put("/me", response_model=UserModel)
def update_profile(update: UserUpdateModel, user=Depends(get_current_user)):
    uid = user["uid"]

    # Update Firestore
    updated_data = update_user_data(uid, update.model_dump(exclude_unset=True))

    return UserModel(
        uid=uid,
        firebase_data=user,
        monthly_salary=updated_data.get("monthly_salary"),
        hourly_pay=updated_data.get("hourly_pay"),
        firestore_data=updated_data
    )