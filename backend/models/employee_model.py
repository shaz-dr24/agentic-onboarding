from config import get_db_connection
import json


# ✅ CREATE EMPLOYEE
def create_employee(name, email, role):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO employees (name, email, role, status)
        VALUES (%s, %s, %s, %s)
        RETURNING id
    """, (name, email, role, "pending"))

    emp_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return emp_id


# ✅ GET EMPLOYEE BY ID (VERY IMPORTANT)
def get_employee_by_id(emp_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, name, email, role, status, extracted_data
        FROM employees
        WHERE id = %s
    """, (emp_id,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return None

    return {
        "id": row[0],
        "name": row[1],
        "email": row[2],
        "role": row[3],
        "status": row[4],
        "extracted_data": row[5]
    }


# ✅ UPDATE EXTRACTED DATA
def update_extracted_data(emp_id, data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE employees
        SET extracted_data = %s
        WHERE id = %s
    """, (json.dumps(data), emp_id))

    conn.commit()
    cur.close()
    conn.close()


# ✅ UPDATE STATUS (PASSED / FAILED)
def update_employee_status(emp_id, status):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE employees
        SET status = %s
        WHERE id = %s
    """, (status, emp_id))

    conn.commit()
    cur.close()
    conn.close()


# ✅ SAVE STRUCTURED FIELDS (FINAL DB STORAGE)
def update_employee_fields(emp_id, data):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE employees
        SET 
            aadhar_number = %s,
            pan_number = %s,
            bank_account = %s,
            tenth_marks = %s,
            twelfth_marks = %s,
            cgpa = %s
        WHERE id = %s
    """, (
        data.get("aadhar_number"),
        data.get("pan_number"),
        data.get("bank_account"),
        data.get("10th_marks"),
        data.get("12th_marks"),
        data.get("cgpa"),
        emp_id
    ))

    conn.commit()
    cur.close()
    conn.close()