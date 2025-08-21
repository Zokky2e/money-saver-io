from firebase_admin import auth
from app.config import db

def calculate_working_hours(price: float, hourly_pay: float):
    return round(price / hourly_pay)