import psycopg2

def get_db_connection():
    return psycopg2.connect(
        dbname="onboarding_ai",
        user="postgres",
        password="Shaz@1234",
        host="localhost",
        port="5432"
    )