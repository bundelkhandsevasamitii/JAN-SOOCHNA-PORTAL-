"""
Central Firebase connection for the whole Python/Flask project.
Frontend files NEVER contain Firebase credentials or SDK configuration.
Set FIREBASE_SERVICE_ACCOUNT to the path of your Firebase service-account JSON.
"""
import os
from functools import lru_cache

@lru_cache(maxsize=1)
def get_db():
    service_account_path = os.getenv("FIREBASE_SERVICE_ACCOUNT", "serviceAccountKey.json")
    if not os.path.exists(service_account_path):
        return None

    try:
        import firebase_admin
        from firebase_admin import credentials, firestore
        if not firebase_admin._apps:
            cred = credentials.Certificate(service_account_path)
            firebase_admin.initialize_app(cred)
        return firestore.client()
    except Exception as exc:
        print(f"[Firebase] Connection error: {exc}")
        return None

def get_portal_stats():
    """Reads optional public summary values from Firestore; safe demo defaults otherwise."""
    db = get_db()
    if db is None:
        return {
            "states": "36",
            "districts": "—",
            "villages": "—",
            "notices": "0",
            "source": "Demo data — Firebase not connected"
        }

    try:
        doc = db.collection("portal_public").document("stats").get()
        if doc.exists:
            data = doc.to_dict() or {}
            return {
                "states": data.get("states", "36"),
                "districts": data.get("districts", "—"),
                "villages": data.get("villages", "—"),
                "notices": data.get("notices", "0"),
                "source": "Firestore"
            }
    except Exception as exc:
        print(f"[Firebase] Stats read error: {exc}")

    return {"states": "36", "districts": "—", "villages": "—", "notices": "0",
            "source": "Default values — stats not published"}

def get_latest_notices(limit=5):
    db = get_db()
    if db is None:
        return []
    try:
        docs = (db.collection("notices")
                  .where("published", "==", True)
                  .order_by("created_at", direction="DESCENDING")
                  .limit(limit).stream())
        results = []
        for doc in docs:
            item = doc.to_dict() or {}
            results.append({
                "title": item.get("title", "सूचना"),
                "department": item.get("department", "सामान्य प्रशासन"),
                "date": item.get("date", "")
            })
        return results
    except Exception as exc:
        print(f"[Firebase] Notice read error: {exc}")
        return []
