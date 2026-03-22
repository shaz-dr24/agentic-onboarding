from models.employee_model import (
    get_employee_by_id,
    update_employee_status
)
from agents.verification_agent import verify_employee
from services.n8n_service import call_n8n
import json


def run_onboarding(emp_id):

    print(f"\n🚀 Starting onboarding for Employee ID: {emp_id}")

    # -----------------------------------
    # 🔥 FETCH EMPLOYEE DATA FROM DB
    # -----------------------------------
    employee = get_employee_by_id(emp_id)

    if not employee or not employee.get("extracted_data"):
        print("❌ No extracted data found")

        update_employee_status(emp_id, "failed")

        # send minimal failure payload
        call_n8n(
            "http://localhost:5678/webhook/onboarding",
            {
                "employee_id": emp_id,
                "status": "failed",
                "name": employee.get("name") if employee else "Candidate",
                "email": employee.get("email") if employee else None,
                "reasons": ["No extracted data found"]
            }
        )

        return "failed"

    # -----------------------------------
    # 🔥 PARSE JSON DATA
    # -----------------------------------
    data = employee["extracted_data"]

    if isinstance(data, str):
        data = json.loads(data)

    print("🔥 FINAL DATA USED:", data)

    # -----------------------------------
    # 🧠 VERIFY DATA
    # -----------------------------------
    status, reasons = verify_employee(data)

    print(f"✅ Verification Status: {status}")
    print(f"⚠️ Reasons: {reasons}")

    # -----------------------------------
    # 🧑 SAFE VALUES
    # -----------------------------------
    name = data.get("name") or employee.get("name") or "Candidate"
    email = data.get("email") or employee.get("email") or None

    clean_name = "".join(name.lower().split())

    # -----------------------------------
    # 📦 COMMON PAYLOAD
    # -----------------------------------
    payload = {
        "employee_id": emp_id,
        "status": status,
        "name": name,
        "email": email,
        "reasons": reasons
    }

    # -----------------------------------
    # ❌ FAILURE FLOW
    # -----------------------------------
    if status == "failed":

        update_employee_status(emp_id, "failed")

        print("📡 Sending FAILURE to n8n:", payload)

        call_n8n(
            "http://localhost:5678/webhook/onboarding",
            payload
        )

        return "failed"

    # -----------------------------------
    # ✅ SUCCESS FLOW
    # -----------------------------------
    company_email = f"{clean_name}@company.com"
    password = "Welcome@123"

    payload.update({
        "company_email": company_email,
        "password": password,
        "task": "Complete onboarding training"
    })

    update_employee_status(emp_id, "passed")

    print("📡 Sending SUCCESS to n8n:", payload)

    call_n8n(
        "http://localhost:5678/webhook/onboarding",
        payload
    )

    return "completed"