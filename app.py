import os

from flask import Flask, render_template, jsonify
from firebase import db

app = Flask(__name__)

# =====================================
# BHARAT JAN SUCHNA PORTAL
# MAIN SERVER
# =====================================


# HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# FIREBASE CONNECTION STATUS
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


# PORTAL STATISTICS
@app.route("/api/stats")
def api_stats():

    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    return jsonify({
        "status": "success",
        "message": "Statistics API is ready"
    })


# LATEST NOTICES
@app.route("/api/notices")
def api_notices():

    if db is None:
        return jsonify({"error": "Database unavailable"}), 503

    return jsonify({
        "status": "success",
        "notices": []
    })


# HEALTH CHECK
@app.route("/health")
def health():

    return jsonify({
        "status": "ok",
        "message": "Bharat Jan Suchna Portal is running"
    })


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
