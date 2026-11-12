import os
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from firebase import db

app = Flask(__name__)

# =====================================
# BHARAT JAN SUCHNA PORTAL
# MAIN SERVER
# =====================================


# =====================================
# 1. HTML PAGE ROUTES (FRONTEND)
# =====================================

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/village")
def village_page():
    return render_template("village.html")


@app.route("/schemes")
def schemes_page():
    return render_template("schemes.html")


@app.route("/budget")
def budget_page():
    return render_template("budget.html")


@app.route("/notices")
def notices_page():
    return render_template("notices.html")


@app.route("/complaints")
def complaints_page():
    return render_template("complaints.html")


@app.route("/reports")
def reports_page():
    return render_template("reports.html")


# =====================================
# 2. SYSTEM & HEALTH APIs
# =====================================

@app.route("/api/firebase")
def firebase_status():
    if db is None:
        return jsonify({
            "status": "error",
            "firebase": "disconnected"
        }), 503

    return jsonify({
        "status": "success",
        "firebase": "connected"
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "message": "Bharat Jan Suchna Portal is running"
    })


# =====================================
# 3. PORTAL DATA APIs (FIREBASE READY)
# =====================================

# HOME PAGE: PORTAL STATISTICS
@app.route("/api/stats")
def api_stats():
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    return jsonify({
        "status": "success",
        "message": "Statistics API is ready",
        "data": {
            "total_schemes": 0,
            "total_budget": "₹0",
            "resolved_complaints": 0,
            "active_notices": 0
        }
    })


# VILLAGE PROFILE & INFRASTRUCTURE API
@app.route("/api/village", methods=["GET"])
def api_village():
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    try:
        # Firebase Firestore से 'village_info' कलेक्शन या डॉक्यूमेंट लाएं
        docs = db.collection("village_info").stream()
        village_data = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return jsonify({"status": "success", "village": village_data})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# GOVERNMENT SCHEMES (योजनाएं) API
@app.route("/api/schemes", methods=["GET"])
def api_schemes():
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    try:
        docs = db.collection("schemes").stream()
        schemes_list = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return jsonify({"status": "success", "schemes": schemes_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# PANCHAYAT BUDGET & FUNDS (बजट) API
@app.route("/api/budget", methods=["GET"])
def api_budget():
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    try:
        docs = db.collection("budget").stream()
        budget_list = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return jsonify({"status": "success", "budget": budget_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# LATEST NOTICES (सूचनाएं) API
@app.route("/api/notices", methods=["GET"])
def api_notices():
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    try:
        docs = db.collection("notices").stream()
        notices_list = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return jsonify({"status": "success", "notices": notices_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# CITIZEN COMPLAINTS (शिकायत दर्ज करें और देखें) API
@app.route("/api/complaints", methods=["GET", "POST"])
def api_complaints():
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    # नई शिकायत दर्ज करने के लिए (POST)
    if request.method == "POST":
        data = request.get_json()
        if not data or not data.get("title") or not data.get("description"):
            return jsonify({"status": "error", "message": "Title and description required"}), 400

        try:
            complaint_data = {
                "name": data.get("name", "Anonymous"),
                "ward": data.get("ward", ""),
                "title": data.get("title"),
                "description": data.get("description"),
                "status": "Pending",
                "created_at": datetime.utcnow().isoformat()
            }
            _, doc_ref = db.collection("complaints").add(complaint_data)
            return jsonify({
                "status": "success",
                "message": "Complaint registered successfully",
                "complaint_id": doc_ref.id
            }), 201
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500

    # सभी शिकायतें देखने के लिए (GET)
    try:
        docs = db.collection("complaints").stream()
        complaints_list = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return jsonify({"status": "success", "complaints": complaints_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# DEVELOPMENT REPORTS (विकास रिपोर्ट्स) API
@app.route("/api/reports", methods=["GET"])
def api_reports():
    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    try:
        docs = db.collection("reports").stream()
        reports_list = [{**doc.to_dict(), "id": doc.id} for doc in docs]
        return jsonify({"status": "success", "reports": reports_list})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# =====================================
# ERROR HANDLERS (404)
# =====================================

@app.errorhandler(404)
def page_not_found(e):
    return jsonify({
        "status": "error",
        "message": "Page or API endpoint not found"
    }), 404


# =====================================
# SERVER START
# =====================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
