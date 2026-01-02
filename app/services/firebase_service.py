from fastapi import HTTPException
import requests
from firebase_admin import auth, firestore
from app.config import db, FIREBASE_API_KEY

def verify_token(id_token: str):
    """
    Verifies Firebase ID token from frontend and returns decoded user info.
    """
    decoded_token = auth.verify_id_token(id_token)
    return decoded_token

def get_user_data(uid: str):
    """
    Fetches user data from Firestore.
    """
    doc_ref = db.collection("users").document(uid)
    doc = doc_ref.get()
    return doc.to_dict() if doc.exists else None

def set_user_data(uid: str, data: dict):
    """
    Saves user data to Firestore.
    """
    db.collection("users").document(uid).set(data)

def update_user_data(uid: str, data: dict):
    user_ref = db.collection("users").document(uid)
    user_ref.set(data, merge=True)  # merge=True keeps existing fields
    return user_ref.get().to_dict()

def register_user(email: str, password: str):
    """Register a new user using Firebase Auth REST API"""
    if (len(password) < 7):
        raise HTTPException(status_code=400, detail=str("Password too short."))
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json()


def login_user(email: str, password: str):
    """Login existing user using Firebase Auth REST API"""
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    r = requests.post(url, json=payload)
    r.raise_for_status()
    return r.json()

def refresh_token(refresh_token: str):
    url = "https://securetoken.googleapis.com/v1/token"
    r = requests.post(
        url,
        params={"key": FIREBASE_API_KEY},
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
        },
    )
    new_id_token = r.json()["id_token"]
    return {"id_token": new_id_token}

def create_user_doc(uid: str):
    """Initialize Firestore user doc if not exists"""
    user_ref = db.collection("users").document(uid)
    if not user_ref.get().exists:
        user_ref.set({"monthly_salary": None, "hourly_pay": None, "total_saved": 0.0})