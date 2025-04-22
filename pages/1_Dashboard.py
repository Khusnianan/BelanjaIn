import streamlit as st
from db import get_connection

st.title("📊 Dashboard Penjualan")

conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT COUNT(*) FROM transactions")
total_trans = cur.fetchone()[0]

cur.execute("SELECT COALESCE(SUM(total), 0) FROM transactions")
total_income = cur.fetchone()[0]

st.metric("Total Transaksi", total_trans)
st.metric("Total Pendapatan", f"Rp {total_income:,.0f}")

cur.close()
conn.close()
