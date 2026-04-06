"""
DRTMS Flask REST API Backend
Run: python app.py
API runs on http://localhost:5000
"""
from flask import Flask, jsonify, request
from drtms_core import DRTMS

app = Flask(__name__)

# Single shared DRTMS instance (in-memory)
db = DRTMS()

# ── CORS (no external package needed) ────────────────────────
@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
    return response

@app.route("/api/<path:p>", methods=["OPTIONS"])
def options_handler(p):
    return "", 204


# ── Stats ─────────────────────────────────────────────────────
@app.route("/api/stats", methods=["GET"])
def get_stats():
    return jsonify(db.get_stats())


# ── Resources ─────────────────────────────────────────────────
@app.route("/api/resources", methods=["GET"])
def list_resources():
    return jsonify([r.to_dict() for r in db.resources.values()])


@app.route("/api/resources", methods=["POST"])
def add_resource():
    data = request.json or {}
    ok, msg = db.add_resource(
        data.get("resource_id", "").strip(),
        data.get("name", "").strip(),
        data.get("resource_type", "").strip(),
        int(data.get("quantity", 0)),
        data.get("unit", "").strip(),
    )
    status = 201 if ok else 400
    return jsonify({"success": ok, "message": msg}), status


# ── Disasters ─────────────────────────────────────────────────
@app.route("/api/disasters", methods=["GET"])
def list_disasters():
    return jsonify([d.to_dict() for d in db.disasters.values()])


@app.route("/api/disasters", methods=["POST"])
def register_disaster():
    data = request.json or {}
    try:
        severity = int(data.get("severity", 0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Severity must be a number."}), 400
    ok, msg = db.register_disaster(
        data.get("disaster_id", "").strip(),
        data.get("name", "").strip(),
        data.get("location", "").strip(),
        severity,
        data.get("disaster_type", "").strip(),
    )
    status = 201 if ok else 400
    return jsonify({"success": ok, "message": msg}), status


# ── Allocate ──────────────────────────────────────────────────
@app.route("/api/allocate", methods=["POST"])
def allocate():
    data = request.json or {}
    try:
        qty = int(data.get("quantity", 0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Quantity must be a number."}), 400
    ok, msg = db.allocate_resource(
        data.get("disaster_id", "").strip(),
        data.get("resource_id", "").strip(),
        qty,
    )
    status = 200 if ok else 400
    return jsonify({"success": ok, "message": msg}), status


# ── Release ───────────────────────────────────────────────────
@app.route("/api/release", methods=["POST"])
def release():
    data = request.json or {}
    try:
        qty = int(data.get("quantity", 0))
    except (ValueError, TypeError):
        return jsonify({"success": False, "message": "Quantity must be a number."}), 400
    ok, msg = db.release_resource(
        data.get("disaster_id", "").strip(),
        data.get("resource_id", "").strip(),
        qty,
    )
    status = 200 if ok else 400
    return jsonify({"success": ok, "message": msg}), status


# ── Log ───────────────────────────────────────────────────────
@app.route("/api/log", methods=["GET"])
def get_log():
    return jsonify(db.allocation_log)


# ── Test Cases ────────────────────────────────────────────────
@app.route("/api/tests", methods=["POST"])
def run_tests():
    results = db.run_test_cases()
    return jsonify(results)


# ── Reset ─────────────────────────────────────────────────────
@app.route("/api/reset", methods=["POST"])
def reset():
    global db
    db = DRTMS()
    return jsonify({"success": True, "message": "System reset to initial state."})


if __name__ == "__main__":
    print("=" * 55)
    print("  DRTMS API Server")
    print("  http://localhost:5000")
    print("=" * 55)
    app.run(debug=True, port=5000)
