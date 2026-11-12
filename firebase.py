import os
import json
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage


# ==========================================
# BHARAT JAN SUCHNA PORTAL
# FIREBASE CONFIGURATION
# ==========================================

PROJECT_ID = "jan-soochna-portal"

STORAGE_BUCKET = "jan-soochna-portal.firebasestorage.app"


# ==========================================
# FIREBASE INITIALIZATION
# ==========================================

db = None
bucket = None
firebase_app = None


def initialize_firebase():

    global db, bucket, firebase_app

    try:

        # Get Firebase Service Account
        firebase_json = os.environ.get("FIREBASE_CREDENTIALS")

        if not firebase_json:
            raise ValueError(
                "FIREBASE_CREDENTIALS environment variable missing"
            )

        # Convert JSON String into Dictionary
        service_account_info = json.loads(firebase_json)

        # Verify Project ID
        if service_account_info.get("project_id") != PROJECT_ID:
            raise ValueError("Firebase Project ID does not match")

        # Firebase Credentials
        cred = credentials.Certificate(service_account_info)

        # Initialize Firebase
        try:
            firebase_app = firebase_admin.get_app()

        except ValueError:

            firebase_app = firebase_admin.initialize_app(
                cred,
                {
                    "projectId": PROJECT_ID,
                    "storageBucket": STORAGE_BUCKET
                }
            )

        # Firestore Connection
        db = firestore.client(app=firebase_app)

        # Firebase Storage Connection
        bucket = storage.bucket(app=firebase_app)

        print("================================")
        print("FIREBASE CONNECTED SUCCESSFULLY")
        print("PROJECT:", PROJECT_ID)
        print("FIRESTORE: READY")
        print("STORAGE: READY")
        print("================================")

        return True

    except Exception as e:

        db = None
        bucket = None
        firebase_app = None

        print("FIREBASE CONNECTION FAILED:", str(e))

        raise RuntimeError(
            "Firebase initialization failed"
        ) from e


# ==========================================
# DATABASE COLLECTION
# ==========================================

def get_collection(collection_name):

    if db is None:
        raise RuntimeError("Firestore is not connected")

    return db.collection(collection_name)


# ==========================================
# DATABASE DOCUMENT
# ==========================================

def get_document(collection_name, document_id):

    if db is None:
        raise RuntimeError("Firestore is not connected")

    return db.collection(collection_name).document(document_id)


# ==========================================
# GET DOCUMENT DATA
# ==========================================

def get_document_data(collection_name, document_id):

    document = get_document(
        collection_name,
        document_id
    ).get()

    if document.exists:
        return document.to_dict()

    return None


# ==========================================
# ADD DATABASE DOCUMENT
# ==========================================

def add_document(collection_name, data):

    if db is None:
        raise RuntimeError("Firestore is not connected")

    return db.collection(collection_name).add(data)


# ==========================================
# STORAGE UPLOAD
# ==========================================

def upload_file(file, destination):

    if bucket is None:
        raise RuntimeError("Firebase Storage is not connected")

    blob = bucket.blob(destination)

    blob.upload_from_file(
        file,
        content_type=getattr(file, "content_type", None)
    )

    return blob


# ==========================================
# STORAGE DELETE
# ==========================================

def delete_file(destination):

    if bucket is None:
        raise RuntimeError("Firebase Storage is not connected")

    blob = bucket.blob(destination)

    if blob.exists():
        blob.delete()

    return True


# ==========================================
# FIREBASE CONNECTION START
# ==========================================

initialize_firebase()
