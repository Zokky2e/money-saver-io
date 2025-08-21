from fastapi import APIRouter, Depends
from app.models.money_models import MoneyInput, MoneyOutput
from app.services.firebase_service import set_user_data
from app.dependencies import get_current_user, get_current_user_data
from app.services.money_management_service import calculate_working_hours

router = APIRouter()

@router.post("/", response_model=MoneyOutput)
def post_money_cost(data: MoneyInput, user=Depends(get_current_user)):
    current_user = get_current_user_data(user)
    # Example calculation
    result = calculate_working_hours(data.price, current_user.hourly_pay)

    # Save to Firestore
    #set_user_data(uid, {"last_calculation": {"input": data.price, "result": result}})

    return MoneyOutput(price=data.price, working_hours=result)
