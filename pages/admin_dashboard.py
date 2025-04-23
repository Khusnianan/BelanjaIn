import streamlit as st
from db import add_barang, update_barang, delete_barang

st.title("📊 Dashboard Admin")
st.write("Admin dapat mengelola produk di sini.")

# Form untuk menambah produk baru
with st.form("add_product"):
    st.subheader("Tambah Produk")
    nama = st.text_input("Nama Produk")
    harga = st.number_input("Harga Produk", min_value=0)
    stok = st.number_input("Stok Produk", min_value=0)
    add_button = st.form_submit_button("Tambah Produk")
    if add_button:
        add_barang(nama, harga, stok)
        st.success("Produk berhasil ditambahkan!")

# Daftar produk yang ada
st.subheader("Daftar Produk")
produk = get_all_barang()
for index, row in produk.iterrows():
    with st.expander(f"Produk: {row['nama']}"):
        # Update produk
        new_nama = st.text_input("Nama", value=row['nama'])
        new_harga = st.number_input("Harga", value=row['harga'])
        new_stok = st.number_input("Stok", value=row['stok'])
        update_button = st.button(f"Update {row['nama']}")
        if update_button:
            update_barang(row['id'], new_nama, new_harga, new_stok)
            st.success(f"Produk {row['nama']} berhasil diupdate!")
        
        # Hapus produk
        delete_button = st.button(f"Hapus {row['nama']}")
        if delete_button:
            delete_barang(row['id'])
            st.success(f"Produk {row['nama']} berhasil dihapus!")
