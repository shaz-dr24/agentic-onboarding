from flask import Blueprint, request, jsonify
import os

from models.employee_model import (
    create_employee,
    update_extracted_data,
    update_employee_fields
)
from models.document_model import save_document

from services.parser_service import extract_text
from services.extraction_service import extract_details
from services.merge_service import merge_data
from services.onboarding_service import run_onboarding

employee_bp = Blueprint("employee", __name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@employee_bp.route("/upload_employee", methods=["POST"])
def upload_employee():
    try:
        # -------------------------------
        # 📋 Basic details
        # -------------------------------
        name = request.form.get("name")
        email = request.form.get("email")
        role = request.form.get("role")

        if not name or not email or not role:
            return jsonify({"error": "Missing required fields"}), 400

        # -------------------------------
        # 👤 Create employee
        # -------------------------------
        emp_id = create_employee(name, email, role)

        files = request.files.getlist("documents")
        doc_types = request.form.getlist("doc_types")

        if len(files) != len(doc_types):
            return jsonify({"error": "documents and doc_types mismatch"}), 400

        combined_data = {}

        # -------------------------------
        # 🔁 Process documents
        # -------------------------------
        for file, doc_type in zip(files, doc_types):

            if file.filename == "":
                continue

            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            save_document(emp_id, doc_type, file_path)

            text = extract_text(file_path)
            extracted = extract_details(text)

            print(f"📄 Extracted from {doc_type}:", extracted)

            combined_data = merge_data(combined_data, extracted)

        # -------------------------------
        # 💾 Store in DB
        # -------------------------------
        if combined_data:
            print("🔥 FINAL EXTRACTED DATA:", combined_data)

            update_extracted_data(emp_id, combined_data)
            update_employee_fields(emp_id, combined_data)

        # -------------------------------
        # 🚀 Trigger onboarding
        # -------------------------------
        onboarding_status = run_onboarding(emp_id)

        return jsonify({
            "message": "Employee processed successfully",
            "employee_id": emp_id,
            "extracted_data": combined_data,
            "onboarding_status": onboarding_status
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employee_bp.route("/add_employee", methods=["POST"])
def add_employee():
    data = request.json

    emp_id = create_employee(
        data["name"],
        data["email"],
        data["role"]
    )

    return jsonify({"employee_id": emp_id})