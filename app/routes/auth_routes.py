from fastapi import APIRouter, Depends, HTTPException
from app.models.auth_models import LoginModel, RegisterModel
from app.models.user_models import UserModel, UserUpdateModel
from app.services.firebase_service import *
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

@router.post("/register")
def register(data: RegisterModel):
    try:
        result = register_user(data.email, data.password)
        uid = result["localId"]
        create_user_doc(uid)  # prepare Firestore doc
        return {"message": "User registered successfully", "uid": uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login(data: LoginModel):
    try:
        result = login_user(data.email, data.password)
        # result contains idToken, refreshToken, localId
        return {
            "idToken": result["idToken"],
            "refreshToken": result["refreshToken"],
            "uid": result["localId"],
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))