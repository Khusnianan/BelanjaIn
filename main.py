import streamlit as st
from auth import login, register

st.set_page_config(page_title="Belanja-in", layout="wide")

menu = st.sidebar.selectbox("Menu", ["Login", "Register"])

if menu == "Login":
    login()
elif menu == "Register":
    register()
