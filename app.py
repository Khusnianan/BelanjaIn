import streamlit as st

# Konfigurasi halaman HARUS di awal
st.set_page_config(
    page_title="BelanjaIn - Toko Online",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

from utils.auth_utils import is_logged_in, authenticate
from utils.navigation import tampilkan_navbar

# CSS untuk tampilan
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .login-container {
        max-width: 500px;
        margin: 2rem auto;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

def tampilkan_form_login():
    """Menampilkan form login yang jelas"""
    with st.container():
        st.markdown("""
        <div class="login-container">
            <h2 style="text-align: center;">Login ke BelanjaIn</h2>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("form_login"):
            username = st.text_input("Username", placeholder="Masukkan username Anda")
            password = st.text_input("Password", type="password", placeholder="Masukkan password Anda")
            
            if st.form_submit_button("MASUK"):
                pengguna = authenticate(username, password)
                if pengguna:
                    st.session_state.user = pengguna
                    st.rerun()
                else:
                    st.error("Username atau password salah")
        
        st.markdown("""
        <div style="text-align: center; margin-top: 1rem;">
            Belum punya akun? <a href="/profil" target="_self">Daftar disini</a>
        </div>
        """, unsafe_allow_html=True)

def main():
    # Inisialisasi session state jika belum ada
    if 'user' not in st.session_state:
        st.session_state.user = None
    
    # Tampilkan navbar
    tampilkan_navbar()
    
    # Debugging: Tampilkan status login
    st.write("Status Login:", is_logged_in())
    
    # Tampilkan form login jika belum login
    if not is_logged_in():
        tampilkan_form_login()
    else:
        st.success("Anda sudah login!")
        if st.button("Logout"):
            from utils.auth_utils import logout
            logout()

if __name__ == "__main__":
    main()
