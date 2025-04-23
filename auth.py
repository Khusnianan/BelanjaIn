import streamlit as st
import bcrypt
from db import get_connection

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def check_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def login():
    st.subheader("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password FROM users WHERE email=%s", (email,))
        result = cur.fetchone()
        cur.close()
        conn.close()

        if result and check_password(password, result[1].encode()):
            st.success("Login berhasil!")
            # Simpan user ke session state
            st.session_state["logged_in"] = True
            st.session_state["user_id"] = result[0]
            st.experimental_rerun()  # refresh halaman supaya pindah ke dashboard
        else:
            st.error("Login gagal. Email atau password salah.")
            
def register():
    st.subheader("Register")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        hashed = hash_password(password)
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed.decode()))
        conn.commit()
        cur.close()
        conn.close()
        st.success("Registrasi berhasil!")
