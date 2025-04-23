import streamlit as st
from db import get_all_barang
from auth import login_user, hash_password

st.set_page_config(page_title="BelanjaIn", layout="wide")

st.title("🛍️ BelanjaIn - Toko Online")

st.subheader("📦 Daftar Barang")
barang_df = get_all_barang()
st.dataframe(barang_df, use_container_width=True)

st.markdown("---")
st.subheader("🔐 Login")

login_col1, login_col2, login_col3 = st.columns(3)

with login_col1:
    if st.button("Login Admin"):
        st.session_state.login_role = "admin"
with login_col2:
    if st.button("Login Kasir"):
        st.session_state.login_role = "kasir"
with login_col3:
    if st.button("Login Pelanggan"):
        st.session_state.login_role = "pelanggan"

if "login_role" in st.session_state:
    with st.form("login_form"):
        st.write(f"Login sebagai {st.session_state.login_role}")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted:
            user = login_user(username, password)
            if user and user["role"] == st.session_state.login_role:
                st.success(f"Berhasil login sebagai {user['username']} ({user['role']})")
                st.session_state.user = user
                st.switch_page(f"pages/{user['role']}_dashboard.py")
            else:
                st.error("Username/password salah atau role tidak cocok.")
