import streamlit as st
import hashlib
from utils.db import db
from utils.session_manager import SessionState

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate(username, password, state):
    """Fungsi login yang independen"""
    try:
        hashed = hash_password(password)
        user = db.execute_query(
            "SELECT * FROM users WHERE username = %s AND password = %s",
            (username, hashed),
            fetch_one=True
        )
        if user:
            state.user = user
            st.session_state.user = user
            return True
        return False
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return False

def tampilkan_form_login(state):
    """Form login yang standalone"""
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login"):
            if authenticate(username, password, state):
                st.rerun()
            else:
                st.error("Login gagal")

def logout(state):
    """Fungsi logout independen"""
    state.user = None
    st.session_state.user = None
