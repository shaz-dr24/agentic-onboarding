import re


def verify_employee(data):
    failures = []

    # -----------------------------------
    # 🎓 CGPA
    # -----------------------------------
    try:
        cgpa = float(str(data.get("cgpa", "")).strip())
        if cgpa < 8.3:
            failures.append("CGPA below 8.3")
    except:
        failures.append("Invalid CGPA")

    # -----------------------------------
    # 🆔 Aadhaar
    # -----------------------------------
    aadhar = str(data.get("aadhar_number", "")).replace(" ", "")
    if not re.fullmatch(r"\d{12}", aadhar):
        failures.append("Invalid Aadhaar number")

    # -----------------------------------
    # 💳 PAN
    # -----------------------------------
    pan = str(data.get("pan_number", "")).strip()
    if not re.fullmatch(r"[A-Z]{5}[0-9]{4}[A-Z]", pan):
        failures.append("Invalid PAN number")

    # -----------------------------------
    # 🎓 10th
    # -----------------------------------
    try:
        tenth = float(str(data.get("10th_marks", "")).replace("%", ""))
        if tenth < 75:
            failures.append("10th marks below 75%")
    except:
        failures.append("Invalid 10th marks")

    # -----------------------------------
    # 🎓 12th
    # -----------------------------------
    try:
        twelfth = float(str(data.get("12th_marks", "")).replace("%", ""))
        if twelfth < 75:
            failures.append("12th marks below 75%")
    except:
        failures.append("Invalid 12th marks")

    # -----------------------------------
    # 🏦 Bank Account (10–18 digits realistic)
    # -----------------------------------
    bank = str(data.get("bank_account", "")).strip()
    if not re.fullmatch(r"\d{9,18}", bank):
        failures.append("Invalid bank account number")

    # -----------------------------------
    # FINAL
    # -----------------------------------
    print("🔍 Verification Input:", data)
    print("❌ Failures:", failures)

    if failures:
        return "failed", failures

    return "passed", ["All checks passed"]