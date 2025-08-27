import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials, firestore, auth

# Load environment variables from .env
load_dotenv()

# Get path to service account key
SERVICE_ACCOUNT_PATH = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")

# Get path to firebase api key
FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")

# Initialize Firebase Admin
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)
firebase_admin.initialize_app(cred)

# Firestore client
db = firestore.client()
