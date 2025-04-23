import streamlit as st
from auth import login_form, register_form
from db import get_connection
from models import create_tables

# Konfigurasi halaman
st.set_page_config(page_title="Belanja-in", layout="centered")

# Setup database saat pertama kali dijalankan
conn = get_connection()
create_tables(conn)
conn.close()

# Inisialisasi session state
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# Fungsi untuk top bar di halaman Dashboard
def top_bar_dashboard():
    menu_items = ["Dashboard", "Produk", "Transaksi"]
    active = st.session_state["page"]

    # Membuat top bar dengan tombol: Dashboard, Produk, Transaksi
    col1, col2, col3 = st.columns([2, 2, 2])

    with col1:
        if st.button("Dashboard", key="dashboard"):
            st.session_state["page"] = "dashboard"
            st.rerun()

    with col2:
        if st.button("Produk", key="produk"):
            st.session_state["page"] = "produk"
            st.rerun()

    with col3:
        if st.button("Transaksi", key="transaksi"):
            st.session_state["page"] = "transaksi"
            st.rerun()

    # Menandakan halaman aktif dengan warna
    if active == "dashboard":
        col1.markdown("<div style='height:3px; background-color:#FF4B4B;'></div>", unsafe_allow_html=True)
    elif active == "produk":
        col2.markdown("<div style='height:3px; background-color:#FF4B4B;'></div>", unsafe_allow_html=True)
    elif active == "transaksi":
        col3.markdown("<div style='height:3px; background-color:#FF4B4B;'></div>", unsafe_allow_html=True)

# Fungsi untuk logout
def logout():
    st.session_state["logged_in"] = False
    st.session_state["page"] = "login"
    st.session_state.pop("user_id", None)  # Menghapus user_id
    st.experimental_rerun()

# Cek jika sudah login
if st.session_state["logged_in"]:
    if st.session_state["page"] == "dashboard":
        # Halaman Dashboard
        top_bar_dashboard()  # Tampilkan top bar khusus Dashboard

        st.write("Selamat datang di Dashboard!")
        st.write("Ini adalah halaman dashboard, silakan jelajahi produk kami!")

        # Tombol logout di bagian bawah
        if st.button("Logout"):
            logout()  # Mengeluarkan pengguna

    elif st.session_state["page"] == "produk":
        # Halaman Produk
        top_bar_dashboard()
        st.write("Halaman Produk")
        st.write("Di sini kamu bisa melihat berbagai produk kami.")

    elif st.session_state["page"] == "transaksi":
        # Halaman Transaksi
        top_bar_dashboard()
        st.write("Halaman Transaksi")
        st.write("Di sini kamu bisa melihat histori transaksi yang telah dilakukan.")
else:
    # Jika belum login, tampilkan halaman login atau register
    if st.session_state["page"] == "login":
        login_form()
    elif st.session_state["page"] == "register":
        register_form()
