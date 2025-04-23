import streamlit as st
from db import get_connection
from utils import hash_password, check_password

def login_form():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_password")

    if st.button("Login"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE email=%s", (email,))
        result = cur.fetchone()
        conn.close()

        if result and check_password(password, result[1].encode()):
            st.success("Login berhasil!")
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = result[0]
            st.experimental_rerun()
        else:
            st.error("Email atau password salah.")

def register_form():
    st.subheader("Daftar Akun Baru")
    email = st.text_input("Email", key="register_email")
    password = st.text_input("Password", type="password", key="register_password")

    if st.button("Register"):
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hash_password(password)))
            conn.commit()
            st.success("Registrasi berhasil! Silakan login.")
            st.session_state["page"] = "login"
        except:
            st.error("Email sudah digunakan.")
        finally:
            conn.close()
