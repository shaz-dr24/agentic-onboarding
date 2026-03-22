from config import get_db_connection


def save_document(emp_id, doc_type, file_path):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO documents (employee_id, doc_type, file_path)
        VALUES (%s, %s, %s)
    """, (emp_id, doc_type, file_path))

    conn.commit()
    cur.close()
    conn.close()


def get_documents(emp_id):
    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT doc_type, file_path, status
        FROM documents
        WHERE employee_id=%s
    """, (emp_id,))

    data = cur.fetchall()

    cur.close()
    conn.close()

    return data