import streamlit as st
import hashlib
from utils.db import db

def hash_password(password):
    """Enkripsi password dengan SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    """Verifikasi kredensial login"""
    if not username or not password:
        return None
        
    hashed_password = hash_password(password)
    return db.execute_query(
        "SELECT * FROM users WHERE username = %s AND password = %s",
        (username, hashed_password),
        fetch_one=True
    )

def register_user(username, password, email, nama_lengkap, alamat=None, telepon=None):
    """Pendaftaran pengguna baru"""
    # Implementasi pendaftaran

def get_current_user():
    """Mengambil data pengguna yang login"""
    return st.session_state.get('user')

def is_logged_in():
    """Memeriksa status login"""
    return 'user' in st.session_state

def is_admin():
    """Memeriksa apakah pengguna adalah admin"""
    user = get_current_user()
    return user and user.get('role') == 'admin'

def logout():
    """Proses logout pengguna"""
    if 'user' in st.session_state:
        del st.session_state['user']
    st.rerun()
