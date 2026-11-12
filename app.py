import os
from flask import Flask, render_template, jsonify
from firebase import get_db, get_portal_stats, get_latest_notices

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/stats")
def api_stats():
    return jsonify(get_portal_stats())

@app.route("/api/notices")
def api_notices():
    return jsonify(get_latest_notices())

@app.route("/health")
def health():
    return jsonify({"status": "ok", "message": "Bharat Jan Suchna Portal is running"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
