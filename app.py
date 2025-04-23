# app.py
import streamlit as st
from utils.auth import is_logged_in, is_admin, get_current_user, authenticate, register_user, logout
from utils.db import db

st.set_page_config(
    page_title="BelanjaIn - Toko Online",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS untuk menyembunyikan sidebar
hide_sidebar_style = """
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

# CSS untuk navigation bar
nav_style = """
    <style>
        .navbar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px 20px;
            background-color: #FF4B4B;
            color: white;
            position: sticky;
            top: 0;
            z-index: 1000;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .navbar-brand {
            font-weight: bold;
            font-size: 1.5em;
        }
        .navbar-links {
            display: flex;
            gap: 20px;
        }
        .navbar-link {
            color: white;
            text-decoration: none;
            padding: 5px 10px;
            border-radius: 5px;
        }
        .navbar-link:hover {
            background-color: rgba(255,255,255,0.1);
        }
        .login-container {
            max-width: 400px;
            margin: 50px auto;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
    </style>
"""

def show_navbar():
    st.markdown(nav_style, unsafe_allow_html=True)
    
    if is_logged_in():
        user = get_current_user()
        links = [
            ("🏠 Beranda", "pages/1_🏠_Beranda.py"),
            ("🛒 Produk", "pages/2_🛒_Produk.py"),
            ("📦 Pesanan", "pages/3_📦_Pesanan.py"),
            ("👤 Profil", "pages/4_👤_Profil.py")
        ]
        
        if is_admin():
            links.append(("⚙️ Admin", "pages/5_⚙️_Admin.py"))
        
        nav_html = f"""
        <div class="navbar">
            <div class="navbar-brand">BelanjaIn 🛍️</div>
            <div class="navbar-links">
                {"".join([f'<a href="{link[1]}" class="navbar-link">{link[0]}</a>' for link in links])}
                <a href="#" onclick="logout()" class="navbar-link">Logout</a>
            </div>
        </div>
        <script>
            function logout() {{
                window.parent.postMessage({{type: 'streamlit:setComponentValue', key: 'logout', value: true}}, '*');
            }}
        </script>
        """
    else:
        nav_html = """
        <div class="navbar">
            <div class="navbar-brand">BelanjaIn 🛍️</div>
            <div class="navbar-links">
                <a href="#login" class="navbar-link">Login</a>
                <a href="pages/4_👤_Profil.py" class="navbar-link">Daftar</a>
            </div>
        </div>
        """
    
    st.markdown(nav_html, unsafe_allow_html=True)
    
    # Handle logout from JavaScript
    if st.session_state.get('logout'):
        logout()
        st.session_state.pop('logout')
        st.experimental_rerun()

def show_login_form():
    st.markdown("""
    <div class="login-container">
        <h2 style="text-align: center;">Login ke BelanjaIn</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        col1, col2, col3 = st.columns([1,2,1])
        with col2:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                
                if submit:
                    user = authenticate(username, password)
                    if user:
                        st.session_state.user = user
                        st.experimental_rerun()
                    else:
                        st.error("Username/password salah")
            
            st.markdown("""
            <div style="text-align: center; margin-top: 20px;">
                Belum punya akun? <a href="pages/4_👤_Profil.py">Daftar sekarang</a>
            </div>
            """, unsafe_allow_html=True)

def show_home_content():
    st.title("Selamat datang di BelanjaIn! 🛍️")
    st.markdown("""
    BelanjaIn adalah platform belanja online terbaik untuk kebutuhan sehari-hari.
    
    **Fitur utama:**
    - 🛒 Ribuan produk berkualitas
    - 🚚 Pengiriman cepat
    - 🔒 Transaksi aman
    - 💯 Garansi kepuasan
    
    Silakan login atau daftar untuk mulai berbelanja.
    """)

def main():
    show_navbar()
    
    if not is_logged_in():
        show_login_form()
    else:
        show_home_content()

if __name__ == "__main__":
    main()
