import streamlit as st
from db import get_connection

st.title("🧾 Riwayat Transaksi")

conn = get_connection()
cur = conn.cursor()

cur.execute("""
SELECT t.id, u.email, t.total, t.created_at 
FROM transactions t 
JOIN users u ON t.user_id = u.id 
ORDER BY t.created_at DESC
""")
rows = cur.fetchall()

for row in rows:
    st.write(f"🛒 Transaksi #{row[0]} oleh {row[1]} - Rp{row[2]:,.0f} ({row[3]})")

cur.close()
conn.close()
