import streamlit as st
from auth import login_form, register_form
from db import get_connection
from models import create_tables

# Konfigurasi awal halaman
st.set_page_config(page_title="Belanja-in", layout="centered")

# Setup database saat pertama run
conn = get_connection()
create_tables(conn)
conn.close()

# State halaman (login/register)
if "page" not in st.session_state:
    st.session_state["page"] = "login"

# State login
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# Redirect ke dashboard kalau sudah login
if st.session_state["logged_in"]:
    st.switch_page("pages/1_Dashboard.py")

# Fungsi tampilan bawah (navigasi antar login/register)
def bottom_text():
    if st.session_state["page"] == "login":
        st.markdown(
            "Belum punya akun? <span style='text-decoration: underline; color: #3366cc; cursor: pointer;' onclick='document.dispatchEvent(new CustomEvent(\"switch\", {detail: \"register\"}))'>Sign up</span>",
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            "Sudah punya akun? <span style='text-decoration: underline; color: #3366cc; cursor: pointer;' onclick='document.dispatchEvent(new CustomEvent(\"switch\", {detail: \"login\"}))'>Login</span>",
            unsafe_allow_html=True
        )

# Render halaman login/register
st.title("🛍️ Belanja-in")

if st.session_state["page"] == "login":
    login_form()
elif st.session_state["page"] == "register":
    register_form()

# Spacer + teks link di bawah
st.markdown("<br><br>", unsafe_allow_html=True)
bottom_text()

# Inject JS untuk switch page (karena Streamlit belum support onclick span)
st.markdown("""
<script>
document.addEventListener("switch", function(e) {
    const page = e.detail;
    window.parent.postMessage({type: "streamlit:setComponentValue", value: page}, "*");
});
</script>
""", unsafe_allow_html=True)

# Manual switch handler via hidden input
selected = st.query_params.get("page")
if selected:
    st.session_state["page"] = selected
