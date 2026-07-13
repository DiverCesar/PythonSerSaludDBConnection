import os
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
from db_service.database import patients, doctors, appointments
from db_service.models import serialize

app = Flask(__name__)
CORS(app)


# ── Internal Health Check ────────────────────────────────────────────────────
@app.route("/internal/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200


# ── PATIENTS ─────────────────────────────────────────────────────────────────
@app.route("/internal/patients", methods=["GET"])
def get_patients():
    try:
        data = list(patients.find())
        return jsonify([serialize(d) for d in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/internal/patients", methods=["POST"])
def create_patient():
    try:
        data = request.get_json()
        last = patients.find_one({"id": {"$exists": True}}, sort=[("id", -1)])
        data["id"] = (last["id"] + 1) if last and "id" in last else 1
        data.setdefault("isActive", True)
        result = patients.insert_one(data)
        created = patients.find_one({"_id": result.inserted_id})
        return jsonify(serialize(created)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/internal/patients/<int:item_id>", methods=["PUT"])
def update_patient(item_id):
    try:
        data = request.get_json()
        data.pop("id", None)
        result = patients.find_one_and_update(
            {"id": item_id},
            {"$set": data},
            return_document=True,
        )
        if not result:
            return jsonify({"error": "Patient not found"}), 404
        return jsonify(serialize(result))
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/internal/patients/<int:item_id>", methods=["DELETE"])
def delete_patient(item_id):
    try:
        result = patients.find_one_and_delete({"id": item_id})
        if not result:
            return jsonify({"error": "Patient not found"}), 404
        return jsonify({"message": "Patient deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── DOCTORS ──────────────────────────────────────────────────────────────────
@app.route("/internal/doctors", methods=["GET"])
def get_doctors():
    try:
        data = list(doctors.find())
        return jsonify([serialize(d) for d in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/internal/doctors", methods=["POST"])
def create_doctor():
    try:
        data = request.get_json()
        last = doctors.find_one({"id": {"$exists": True}}, sort=[("id", -1)])
        data["id"] = (last["id"] + 1) if last and "id" in last else 1
        data.setdefault("isActive", True)
        result = doctors.insert_one(data)
        created = doctors.find_one({"_id": result.inserted_id})
        return jsonify(serialize(created)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/internal/doctors/<int:item_id>", methods=["PUT"])
def update_doctor(item_id):
    try:
        data = request.get_json()
        data.pop("id", None)
        result = doctors.find_one_and_update(
            {"id": item_id},
            {"$set": data},
            return_document=True,
        )
        if not result:
            return jsonify({"error": "Doctor not found"}), 404
        return jsonify(serialize(result))
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/internal/doctors/<int:item_id>", methods=["DELETE"])
def delete_doctor(item_id):
    try:
        result = doctors.find_one_and_delete({"id": item_id})
        if not result:
            return jsonify({"error": "Doctor not found"}), 404
        return jsonify({"message": "Doctor deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ── APPOINTMENTS ─────────────────────────────────────────────────────────────
@app.route("/internal/appointments", methods=["GET"])
def get_appointments():
    try:
        data = list(appointments.find())
        return jsonify([serialize(d) for d in data])
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/internal/appointments", methods=["POST"])
def create_appointment():
    try:
        data = request.get_json()
        last = appointments.find_one({"id": {"$exists": True}}, sort=[("id", -1)])
        data["id"] = (last["id"] + 1) if last and "id" in last else 1
        data.setdefault("status", "pending")
        data.setdefault("createdAt", datetime.now().isoformat())
        data.setdefault("isActive", True)
        result = appointments.insert_one(data)
        created = appointments.find_one({"_id": result.inserted_id})
        return jsonify(serialize(created)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/internal/appointments/<int:item_id>", methods=["PUT"])
def update_appointment(item_id):
    try:
        data = request.get_json()
        data.pop("id", None)
        result = appointments.find_one_and_update(
            {"id": item_id},
            {"$set": data},
            return_document=True,
        )
        if not result:
            return jsonify({"error": "Appointment not found"}), 404
        return jsonify(serialize(result))
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/internal/appointments/<int:item_id>", methods=["DELETE"])
def delete_appointment(item_id):
    try:
        result = appointments.find_one_and_delete({"id": item_id})
        if not result:
            return jsonify({"error": "Appointment not found"}), 404
        return jsonify({"message": "Appointment deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
