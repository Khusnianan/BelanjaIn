import streamlit as st
from utils.auth import is_logged_in, is_admin, get_current_user, authenticate

# Konfigurasi halaman
st.set_page_config(
    page_title="BelanjaIn - Toko Online",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS untuk menyembunyikan sidebar dan styling navbar
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 15px;
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
        color: white;
        text-decoration: none;
    }
    .navbar-links {
        display: flex;
        gap: 15px;
    }
    .navbar-link {
        color: white;
        text-decoration: none;
        padding: 8px 12px;
        border-radius: 5px;
        transition: background-color 0.3s;
    }
    .navbar-link:hover {
        background-color: rgba(255,255,255,0.2);
    }
    .login-container {
        max-width: 500px;
        margin: 40px auto;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

def show_navbar():
    """Menampilkan navigation bar di bagian atas"""
    if is_logged_in():
        user = get_current_user()
        links = [
            ("Beranda", "beranda"),
            ("Produk", "produk"),
            ("Pesanan", "pesanan"),
            ("Profil", "profil")
        ]
        
        if is_admin():
            links.append(("Admin", "admin"))
        
        nav_html = f"""
        <div class="navbar">
            <a href="/" class="navbar-brand">BelanjaIn 🛍️</a>
            <div class="navbar-links">
                {"".join([f'<a href="/{link[1]}" class="navbar-link">{link[0]}</a>' for link in links])}
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

def show_login_form():
    """Menampilkan form login di halaman utama"""
    st.markdown("""
    <div class="login-container">
        <h2 style="text-align: center; margin-bottom: 25px;">Login ke BelanjaIn</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        username = st.text_input("Username", placeholder="Masukkan username Anda")
        password = st.text_input("Password", type="password", placeholder="Masukkan password Anda")
        
        if st.form_submit_button("Login", use_container_width=True):
            user = authenticate(username, password)
            if user:
                st.session_state.user = user
                st.rerun()
            else:
                st.error("Username atau password salah")
    
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        Belum punya akun? <a href="/profil" target="_self">Daftar sekarang</a>
    </div>
    """, unsafe_allow_html=True)

def show_home_content():
    """Menampilkan konten utama setelah login"""
    st.title("Selamat datang di BelanjaIn! 🛍️")
    st.markdown("""
    BelanjaIn adalah platform belanja online terbaik untuk kebutuhan sehari-hari.
    
    **Mulai berbelanja sekarang:**
    - Jelajahi berbagai produk berkualitas
    - Proses checkout yang mudah
    - Pengiriman cepat dan aman
    """)

def main():
    try:
        show_navbar()
        
        if not is_logged_in():
            show_login_form()
        else:
            show_home_content()
            
    except Exception as e:
        st.error(f"Terjadi kesalahan: {str(e)}")
        st.button("Coba lagi", on_click=st.rerun)

if __name__ == "__main__":
    main()
