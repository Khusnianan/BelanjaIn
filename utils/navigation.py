import streamlit as st
from utils.auth_utils import is_logged_in, is_admin

def tampilkan_navbar():
    """Navbar yang tidak mengganggu form login"""
    if is_logged_in():
        # Tampilan untuk user yang sudah login
        st.markdown("""
        <div style="display: flex; justify-content: space-between; padding: 1rem; background-color: #FF4B4B; color: white;">
            <div>BelanjaIn 🛍️</div>
            <div>
                <a href="/" style="color: white; margin-right: 1rem;">Beranda</a>
                <a href="/profil" style="color: white; margin-right: 1rem;">Profil</a>
                <a href="#" onclick="logout()" style="color: white;">Logout</a>
            </div>
        </div>
        <script>
            function logout() {
                window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'logout', value: true}, '*');
            }
        </script>
        """, unsafe_allow_html=True)
    else:
        # Tampilan untuk user belum login
        st.markdown("""
        <div style="display: flex; justify-content: space-between; padding: 1rem; background-color: #FF4B4B; color: white;">
            <div>BelanjaIn 🛍️</div>
            <div>
                <a href="#login" style="color: white; margin-right: 1rem;">Login</a>
                <a href="/profil" style="color: white;">Daftar</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
