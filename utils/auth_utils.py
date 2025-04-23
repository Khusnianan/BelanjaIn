import streamlit as st
import hashlib
from utils.db import db

def hash_password(password):
    """Enkripsi password dengan SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    """Fungsi login yang lebih robust"""
    try:
        if not username or not password:
            st.warning("Harap isi username dan password")
            return None
            
        hashed_password = hash_password(password)
        pengguna = db.execute_query(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, hashed_password),
            fetch_one=True
        )
        
        if pengguna:
            return pengguna
        else:
            st.error("Kredensial tidak valid")
            return None
            
    except Exception as e:
        st.error(f"Error saat login: {str(e)}")
        return None

def is_logged_in():
    """Cek login yang lebih akurat"""
    return st.session_state.get('user') is not None
