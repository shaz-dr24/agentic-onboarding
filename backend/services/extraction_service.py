import re


def extract_details(text):

    data = {}

    # Normalize
    text = text.upper()
    text = text.replace("\n", " ")

    # -----------------------------------
    # 📧 Email
    # -----------------------------------
    email = re.findall(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", text)
    if email:
        data["email"] = email[0].lower()

    # -----------------------------------
    # 🆔 Aadhaar
    # -----------------------------------
    aadhar = re.findall(r"\b\d{4}\s\d{4}\s\d{4}\b", text)
    if aadhar:
        data["aadhar_number"] = aadhar[0]

    # -----------------------------------
    # 💳 PAN
    # -----------------------------------
    pan = re.findall(r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", text)
    if pan:
        data["pan_number"] = pan[0]

    # -----------------------------------
    # 🏦 BANK ACCOUNT (STRICT CONTEXT)
    # -----------------------------------
    account = re.findall(
        r"(ACCOUNT\s*NO\.?|A/C\s*NO\.?|ACCOUNT NUMBER)\s*[:\-]?\s*(\d{9,18})",
        text
    )
    if account:
        data["bank_account"] = account[0][1]

    # -----------------------------------
    # 🎓 EDUCATION
    # -----------------------------------
    tenth = re.findall(r"(10TH|SSLC).*?(\d{2,3}\.?\d?\s?%)", text)
    if tenth:
        data["10th_marks"] = tenth[0][1]

    twelfth = re.findall(r"(12TH|HSC).*?(\d{2,3}\.?\d?\s?%)", text)
    if twelfth:
        data["12th_marks"] = twelfth[0][1]

    cgpa = re.findall(r"(CGPA|GPA).*?(\d\.\d{1,2})", text)
    if cgpa:
        data["cgpa"] = cgpa[0][1]

    # -----------------------------------
    # 🧑 NAME (FIXED)
    # -----------------------------------
    name_match = re.findall(r"NAME[:\-]?\s*([A-Z\s]{3,})", text)
    if name_match:
        data["name"] = name_match[0].strip()
    else:
        words = text.split()
        name_words = [w for w in words if w.isalpha() and len(w) > 2]
        if name_words:
            data["name"] = " ".join(name_words[:2])

    return data