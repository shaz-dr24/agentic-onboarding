from config import get_db_connection

def log_step(emp_id, step, status, reason=""):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO logs (employee_id, step, status, reason)
        VALUES (%s, %s, %s, %s)
    """, (emp_id, step, status, reason))

    conn.commit()
    conn.close()