import streamlit as st

# Konfigurasi harus di awal
st.set_page_config(
    page_title="Profil | BelanjaIn",
    page_icon="👤",
    layout="wide"
)

from utils.session_manager import get_session_state
from utils.navigation import tampilkan_navbar

def main():
    state = get_session_state()
    tampilkan_navbar(state)
    
    if state.is_logged_in:
        # Tampilkan halaman profil
        pass
    else:
        # Tampilkan form registrasi
        pass

if __name__ == "__main__":
    main()
