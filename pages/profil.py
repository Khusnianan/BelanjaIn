# pages/4_👤_Profil.py
import streamlit as st
from utils.auth import is_logged_in, get_current_user, register_user, logout
from utils.db import db

st.set_page_config(
    page_title="Profil - BelanjaIn",
    page_icon="👤",
    layout="wide"
)

hide_sidebar_style = """
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

def show_navbar():
    from app import show_navbar
    show_navbar()

def show_register_form():
    st.title("Daftar Akun Baru")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        with col1:
            username = st.text_input("Username*")
            password = st.text_input("Password*", type="password")
            confirm_password = st.text_input("Konfirmasi Password*", type="password")
        with col2:
            email = st.text_input("Email*")
            full_name = st.text_input("Nama Lengkap*")
        
        address = st.text_area("Alamat")
        phone = st.text_input("Nomor Telepon")
        
        submitted = st.form_submit_button("Daftar")
        
        if submitted:
            if not (username and password and confirm_password and email and full_name):
                st.error("Harap isi semua field yang wajib diisi (*)")
            elif password != confirm_password:
                st.error("Password dan konfirmasi password tidak cocok")
            else:
                user = register_user(username, password, email, full_name, address, phone)
                if user:
                    st.success("Pendaftaran berhasil! Anda akan dialihkan ke halaman beranda.")
                    st.session_state.user = user
                    st.experimental_set_query_params(page="home")
                    st.switch_page("app.py")

def show_profile():
    user = get_current_user()
    
    st.title("Profil Saya")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Username", value=user['username'], disabled=True)
            email = st.text_input("Email*", value=user['email'])
        with col2:
            full_name = st.text_input("Nama Lengkap*", value=user['full_name'])
            phone = st.text_input("Nomor Telepon", value=user.get('phone', ''))
        
        address = st.text_area("Alamat", value=user.get('address', ''))
        
        submitted = st.form_submit_button("Update Profil")
        
        if submitted:
            if not (email and full_name):
                st.error("Harap isi semua field yang wajib diisi (*)")
            else:
                db.execute_query(
                    "UPDATE users SET email = %s, full_name = %s, address = %s, phone = %s WHERE user_id = %s",
                    (email, full_name, address, phone, user['user_id'])
                )
                st.success("Profil berhasil diupdate!")
                # Update session
                st.session_state.user = db.execute_query(
                    "SELECT * FROM users WHERE user_id = %s",
                    (user['user_id'],),
                    fetch_one=True
                )
                st.experimental_rerun()

def main():
    show_navbar()
    
    if is_logged_in():
        show_profile()
    else:
        show_register_form()

if __name__ == "__main__":
    main()
