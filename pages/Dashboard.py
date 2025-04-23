import streamlit as st
from db import get_connection

# Menampilkan judul halaman
st.title("📊 Dashboard Penjualan")

# Membuka koneksi ke database
conn = get_connection()
cur = conn.cursor()

# Mengambil jumlah total transaksi
cur.execute("SELECT COUNT(*) FROM transactions")
total_trans = cur.fetchone()[0]

# Mengambil total pendapatan
cur.execute("SELECT COALESCE(SUM(total), 0) FROM transactions")
total_income = cur.fetchone()[0]

# Menampilkan informasi dalam bentuk metrik
st.metric("Total Transaksi", total_trans)
st.metric("Total Pendapatan", f"Rp {total_income:,.0f}")

# Menutup koneksi database
cur.close()
conn.close()
