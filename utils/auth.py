import streamlit as st
import hashlib
from utils.db import db

def hash_password(password):
    """Enkripsi password dengan SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    """Verifikasi login pengguna"""
    if not username or not password:
        return None
        
    hashed_password = hash_password(password)
    pengguna = db.execute_query(
        "SELECT * FROM users WHERE username = %s AND password = %s",
        (username, hashed_password),
        fetch_one=True
    )
    return pengguna

def register_user(username, password, email, nama_lengkap, alamat=None, telepon=None):
    """Mendaftarkan pengguna baru"""
    try:
        # Validasi input
        if len(username) < 5:
            st.error("Username minimal 5 karakter")
            return None
            
        if len(password) < 8:
            st.error("Password minimal 8 karakter")
            return None
            
        # Cek duplikat
        existing = db.execute_query(
            "SELECT * FROM users WHERE username = %s OR email = %s",
            (username, email),
            fetch_one=True
        )
        
        if existing:
            if existing['username'] == username:
                st.error("Username sudah digunakan")
            else:
                st.error("Email sudah terdaftar")
            return None
        
        # Buat user baru
        hashed_password = hash_password(password)
        pengguna = db.execute_query(
            "INSERT INTO users (username, password, email, full_name, address, phone) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
            (username, hashed_password, email, nama_lengkap, alamat, telepon),
            fetch_one=True
        )
        return pengguna
        
    except Exception as e:
        st.error(f"Gagal mendaftar: {str(e)}")
        return None

def get_current_user():
    """Mendapatkan data pengguna yang login"""
    return st.session_state.get('user')

def is_logged_in():
    """Cek status login"""
    return 'user' in st.session_state

def is_admin():
    """Cek apakah admin"""
    return is_logged_in() and st.session_state.user.get('role') == 'admin'

def logout():
    """Proses logout"""
    if 'user' in st.session_state:
        del st.session_state['user']
    st.rerun()
