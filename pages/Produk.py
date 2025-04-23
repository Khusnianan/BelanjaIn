import streamlit as st
from db import get_connection

# Menampilkan judul halaman
st.title("🛍️ Manajemen Produk")

# Membuka koneksi ke database
conn = get_connection()
cur = conn.cursor()

# Form untuk menambah produk
with st.form("Tambah Produk"):
    name = st.text_input("Nama Produk")
    price = st.number_input("Harga", 0)
    stock = st.number_input("Stok", 0, step=1)
    description = st.text_area("Deskripsi")
    
    # Ambil kategori dari database
    cur.execute("SELECT id, name FROM categories")
    categories = cur.fetchall()
    
    # Dropdown untuk memilih kategori produk
    category_id = st.selectbox("Kategori", options=categories, format_func=lambda x: x[1])

    # Tombol submit form
    submit = st.form_submit_button("Simpan")

    # Ketika form disubmit, insert data produk baru ke dalam tabel 'products'
    if submit:
        cur.execute("INSERT INTO products (name, price, stock, description, category_id) VALUES (%s, %s, %s, %s, %s)",
                    (name, price, stock, description, category_id[0]))
        conn.commit()
        st.success("Produk berhasil ditambahkan!")

# Menutup koneksi database
cur.close()
conn.close()
