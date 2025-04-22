import streamlit as st
from db import get_connection

st.title("🛍️ Manajemen Produk")

conn = get_connection()
cur = conn.cursor()

with st.form("Tambah Produk"):
    name = st.text_input("Nama Produk")
    price = st.number_input("Harga", 0)
    stock = st.number_input("Stok", 0, step=1)
    description = st.text_area("Deskripsi")
    cur.execute("SELECT id, name FROM categories")
    categories = cur.fetchall()
    category_id = st.selectbox("Kategori", options=categories, format_func=lambda x: x[1])
    submit = st.form_submit_button("Simpan")

    if submit:
        cur.execute("INSERT INTO products (name, price, stock, description, category_id) VALUES (%s, %s, %s, %s, %s)",
                    (name, price, stock, description, category_id[0]))
        conn.commit()
        st.success("Produk ditambahkan!")

cur.close()
conn.close()
