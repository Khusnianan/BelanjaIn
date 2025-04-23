# app.py
import streamlit as st
from utils.auth import is_logged_in, is_admin
from utils.db import db

st.set_page_config(
    page_title="BelanjaIn - Toko Online",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    st.sidebar.title("BelanjaIn 🛍️")
    
    if not is_logged_in():
        st.sidebar.subheader("Login")
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        
        if st.sidebar.button("Login"):
            from utils.auth import authenticate
            user = authenticate(username, password)
            if user:
                st.session_state.user = user
                st.experimental_rerun()
            else:
                st.sidebar.error("Username/password salah")
        
        st.sidebar.markdown("---")
        st.sidebar.subheader("Belum punya akun?")
        if st.sidebar.button("Daftar Sekarang"):
            st.switch_page("pages/4_👤_Profil.py")
    else:
        user = st.session_state.user
        st.sidebar.success(f"Selamat datang, {user['full_name']}!")
        
        if is_admin():
            st.sidebar.page_link("pages/5_⚙️_Admin.py", label="Admin Dashboard")
        
        st.sidebar.page_link("pages/1_🏠_Beranda.py", label="Beranda")
        st.sidebar.page_link("pages/2_🛒_Produk.py", label="Produk")
        st.sidebar.page_link("pages/3_📦_Pesanan.py", label="Pesanan Saya")
        st.sidebar.page_link("pages/4_👤_Profil.py", label="Profil")
        
        if st.sidebar.button("Logout"):
            from utils.auth import logout
            logout()
    
    st.title("Selamat datang di BelanjaIn!")
    st.markdown("""
        BelanjaIn adalah platform belanja online terbaik untuk kebutuhan sehari-hari.
        
        Silakan login atau daftar untuk mulai berbelanja.
    """)

if __name__ == "__main__":
    main()
