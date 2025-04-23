import streamlit as st
from auth import login, register
from db import get_connection
from models import create_tables

# Setup halaman
st.set_page_config(page_title="Belanja-in", layout="wide")

# Inisialisasi session
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "page" not in st.session_state:
    st.session_state["page"] = "Login"

# Buat tabel saat pertama jalan
conn = get_connection()
create_tables(conn)
conn.close()

# Fungsi untuk render top menu
def top_menu():
    menu_items = ["Login", "Register"]
    cols = st.columns(len(menu_items))

    for i, item in enumerate(menu_items):
        active = st.session_state["page"] == item
        if cols[i].button(item, key=item):
            st.session_state["page"] = item
        if active:
            cols[i].markdown(f"<div style='height:4px; background-color:#ff4b4b;'></div>", unsafe_allow_html=True)
        else:
            cols[i].markdown(f"<div style='height:4px; background-color:transparent;'></div>", unsafe_allow_html=True)

# Tampilkan top nav hanya kalau belum login
if not st.session_state["logged_in"]:
    top_menu()

    if st.session_state["page"] == "Login":
        login()
    elif st.session_state["page"] == "Register":
        register()
else:
    st.switch_page("pages/1_Dashboard.py")
