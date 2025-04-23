import streamlit as st

# HARUS DI AWAL - Konfigurasi halaman
st.set_page_config(
    page_title="BelanjaIn - Toko Online",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import modul setelah konfigurasi
from utils.auth_utils import is_logged_in, is_admin, get_current_user, authenticate, logout
from utils.db import db
from utils.navigation import tampilkan_navbar

# CSS untuk tampilan
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .navbar {
        /* styling navbar */
    }
    .login-container {
        /* styling container login */
    }
</style>
""", unsafe_allow_html=True)

def tampilkan_form_login():
    """Fungsi untuk menampilkan form login"""
    # Implementasi form login

def tampilkan_beranda():
    """Fungsi untuk menampilkan halaman beranda"""
    # Implementasi beranda

def main():
    try:
        tampilkan_navbar()
        if not is_logged_in():
            tampilkan_form_login()
        else:
            tampilkan_beranda()
    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")

if __name__ == "__main__":
    main()
