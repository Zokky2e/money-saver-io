from firebase_admin import auth
from app.config import db

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
