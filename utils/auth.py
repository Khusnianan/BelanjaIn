# utils/auth.py
import streamlit as st
import hashlib
from utils.db import db

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password):
    hashed_password = hash_password(password)
    user = db.execute_query(
        "SELECT * FROM users WHERE username = %s AND password = %s",
        (username, hashed_password),
        fetch_one=True
    )
    return user

def register_user(username, password, email, full_name, address=None, phone=None):
    hashed_password = hash_password(password)
    try:
        user = db.execute_query(
            "INSERT INTO users (username, password, email, full_name, address, phone) "
            "VALUES (%s, %s, %s, %s, %s, %s) RETURNING *",
            (username, hashed_password, email, full_name, address, phone),
            fetch_one=True
        )
        return user
    except Exception as e:
        st.error(f"Registration failed: {e}")
        return None

def get_current_user():
    if 'user' in st.session_state:
        return st.session_state.user
    return None

def is_logged_in():
    return 'user' in st.session_state

def is_admin():
    if is_logged_in():
        return st.session_state.user.get('role') == 'admin'
    return False

def logout():
    if 'user' in st.session_state:
        del st.session_state.user
    st.experimental_rerun()
