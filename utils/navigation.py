import streamlit as st

def tampilkan_navbar(state):
    """Menampilkan navigation bar tanpa impor circular"""
    if state.is_logged_in:
        # Tampilan untuk user yang sudah login
        st.markdown("""
        <div style="display:flex;justify-content:space-between;padding:1rem;background:#FF4B4B;color:white;">
            <div>BelanjaIn 🛍️</div>
            <div>
                <a href="/" style="color:white;margin-right:1rem;">Beranda</a>
                <a href="/profil" style="color:white;">Profil</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Tampilan untuk user belum login
        st.markdown("""
        <div style="display:flex;justify-content:space-between;padding:1rem;background:#FF4B4B;color:white;">
            <div>BelanjaIn 🛍️</div>
            <div>
                <a href="#login" style="color:white;margin-right:1rem;">Login</a>
                <a href="/profil" style="color:white;">Daftar</a>
            </div>
        </div>
        """, unsafe_allow_html=True)
