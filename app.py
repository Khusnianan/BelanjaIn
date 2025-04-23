import streamlit as st

# HARUS DI AWAL - Konfigurasi halaman
st.set_page_config(
    page_title="BelanjaIn - Toko Online",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Import modul setelah konfigurasi
from utils.session_manager import get_session_state
from utils.navigation import tampilkan_navbar

def main():
    state = get_session_state()
    
    # Tampilkan navbar
    tampilkan_navbar(state)
    
    # Konten utama berdasarkan status login
    if not state.is_logged_in:
        from utils.auth_utils import tampilkan_form_login
        tampilkan_form_login(state)
    else:
        st.success(f"Selamat datang, {state.user['full_name']}!")
        if st.button("Logout"):
            from utils.auth_utils import logout
            logout(state)
            st.rerun()

if __name__ == "__main__":
    main()
