import streamlit as st
from db import get_connection

# Menampilkan judul halaman
st.title("🧾 Riwayat Transaksi")

# Membuka koneksi ke database
conn = get_connection()
cur = conn.cursor()

# Query untuk mengambil riwayat transaksi
cur.execute("""
SELECT t.id, u.email, t.total, t.created_at 
FROM transactions t 
JOIN users u ON t.user_id = u.id 
ORDER BY t.created_at DESC
""")
rows = cur.fetchall()

# Menampilkan riwayat transaksi
if rows:
    for row in rows:
        # Menampilkan informasi transaksi
        st.write(f"🛒 **Transaksi #{row[0]}** oleh **{row[1]}**")
        st.write(f"💰 **Total**: Rp {row[2]:,.0f}")
        st.write(f"📅 **Tanggal**: {row[3]}")
        st.write("---")  # Pembatas antar transaksi
else:
    st.write("Tidak ada transaksi yang ditemukan.")

# Menutup koneksi database
cur.close()
conn.close()
