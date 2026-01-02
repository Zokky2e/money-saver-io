from firebase_admin import auth
from app.config import db
from math import ceil

def calculate_working_hours(price: float, hourly_pay: float):
    return ceil(price / hourly_pay)