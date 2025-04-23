import streamlit as st
from utils.auth import is_logged_in, is_admin, get_current_user

def tampilkan_navbar():
    """Menampilkan navigation bar di bagian atas"""
    if is_logged_in():
        pengguna = get_current_user()
        tombol = [
            ("Beranda", "beranda"),
            ("Produk", "produk"), 
            ("Pesanan", "pesanan"),
            ("Profil", "profil")
        ]
        
        if is_admin():
            tombol.append(("Admin", "admin"))
        
        nav_html = f"""
        <div class="navbar">
            <a href="/" class="navbar-brand">BelanjaIn 🛍️</a>
            <div class="navbar-links">
                {"".join([f'<a href="/{link[1]}" class="navbar-link">{link[0]}</a>' for link in tombol])}
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
            <a href="/" class="navbar-brand">BelanjaIn 🛍️</a>
            <div class="navbar-links">
                <a href="#login" class="navbar-link">Login</a>
                <a href="/profil" class="navbar-link">Daftar</a>
            </div>
        </div>
        """
    
    st.markdown(nav_html, unsafe_allow_html=True)
    
    # Handle logout dari JavaScript
    if st.session_state.get('logout'):
        from utils.auth import logout
        logout()
        st.session_state.pop('logout')
        st.rerun()
