import psycopg2
import pandas as pd

DB_URL = "postgresql://postgres:iguefKwACKrTVamieBDyZxcjTKNDVcEG@maglev.proxy.rlwy.net:40486/railway"

def get_conn():
    return psycopg2.connect(DB_URL)

def get_user(username):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("SELECT id, username, password, role FROM users WHERE username = %s", (username,))
        row = cur.fetchone()
        if row:
            return {"id": row[0], "username": row[1], "password": row[2], "role": row[3]}
    return None

def get_all_barang():
    with get_conn() as conn:
        return pd.read_sql("SELECT * FROM barang ORDER BY nama", conn)
