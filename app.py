import streamlit as st

# KONFIGURASI HALAMAN (HARUS DI AWAL)
st.set_page_config(
    page_title="BelanjaIn - Toko Online",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import library dan modul
from utils.auth import is_logged_in, is_admin, get_current_user, authenticate, logout
from utils.db import db
from utils.navigation import tampilkan_navbar

# CSS untuk tampilan
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
        background-color: #FF4B4B;
        color: white;
        position: sticky;
        top: 0;
        z-index: 1000;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    .navbar-brand {
        font-weight: bold;
        font-size: 1.5em;
        color: white;
        text-decoration: none;
    }
    .login-container {
        max-width: 500px;
        margin: 40px auto;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def tampilkan_form_login():
    """Menampilkan form login"""
    st.markdown("""
    <div class="login-container">
        <h2 style="text-align: center; margin-bottom: 25px;">Login ke BelanjaIn</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_login"):
        username = st.text_input("Username", placeholder="Masukkan username Anda")
        password = st.text_input("Password", type="password", placeholder="Masukkan password Anda")
        
        if st.form_submit_button("Login", use_container_width=True):
            pengguna = authenticate(username, password)
            if pengguna:
                st.session_state.user = pengguna
                st.rerun()
            else:
                st.error("Username atau password salah")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        Belum punya akun? <a href="/profil" target="_self">Daftar sekarang</a>
    </div>
    """, unsafe_allow_html=True)

def tampilkan_beranda():
    """Menampilkan halaman beranda"""
    st.title("Selamat datang di BelanjaIn! 🛍️")
    st.markdown("""
    BelanjaIn adalah platform belanja online terbaik untuk kebutuhan sehari-hari.
    
    **Fitur utama:**
    - 🛒 Ribuan produk berkualitas
    - 🚚 Pengiriman cepat
    - 🔒 Transaksi aman
    - 💯 Garansi kepuasan
    
    Silakan jelajahi katalog produk kami.
    """)

def main():
    try:
        # Tampilkan navbar
        tampilkan_navbar()
        
        # Tampilkan konten berdasarkan status login
        if not is_logged_in():
            tampilkan_form_login()
        else:
            tampilkan_beranda()
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
        st.button("Coba lagi", on_click=st.rerun)

if __name__ == "__main__":
    main()
