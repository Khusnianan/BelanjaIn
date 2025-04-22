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
        cur.execute("SELECT password FROM users WHERE email=%s", (email,))
        result = cur.fetchone()
        if result and check_password(password, result[0].encode()):
            st.success("Login berhasil!")
        else:
            st.error("Login gagal.")
        cur.close()
        conn.close()

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
