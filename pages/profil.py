import streamlit as st
from utils.auth import is_logged_in, get_current_user, register_user
from utils.db import db

# Konfigurasi halaman
st.set_page_config(
    page_title="Profil | BelanjaIn",
    page_icon="👤",
    layout="wide"
)

# Sembunyikan sidebar
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

def show_profile():
    """Menampilkan halaman profil pengguna"""
    user = get_current_user()
    
    st.title("Profil Saya 👤")
    
    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.text_input("Username", value=user['username'], disabled=True)
            email = st.text_input("Email*", value=user['email'])
        
        with col2:
            full_name = st.text_input("Nama Lengkap*", value=user['full_name'])
            phone = st.text_input("Nomor Telepon", value=user.get('phone', ''))
        
        address = st.text_area("Alamat", value=user.get('address', ''))
        
        if st.form_submit_button("Simpan Perubahan"):
            if not (email and full_name):
                st.error("Harap isi field yang wajib (*)")
            else:
                db.execute_query(
                    "UPDATE users SET email = %s, full_name = %s, address = %s, phone = %s WHERE user_id = %s",
                    (email, full_name, address, phone, user['user_id'])
                )
                st.success("Profil berhasil diperbarui!")
                st.rerun()

def show_register_form():
    """Menampilkan form pendaftaran"""
    st.title("Daftar Akun Baru 📝")
    
    with st.form("register_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username*", help="Minimal 5 karakter")
            password = st.text_input("Password*", type="password", help="Minimal 8 karakter")
            confirm_password = st.text_input("Konfirmasi Password*", type="password")
        
        with col2:
            email = st.text_input("Email*", help="Gunakan email aktif")
            full_name = st.text_input("Nama Lengkap*")
        
        address = st.text_area("Alamat")
        phone = st.text_input("Nomor Telepon")
        
        if st.form_submit_button("Daftar Sekarang"):
            # Validasi input
            if not all([username, password, confirm_password, email, full_name]):
                st.error("Harap isi semua field wajib (*)")
            elif len(username) < 5:
                st.error("Username minimal 5 karakter")
            elif len(password) < 8:
                st.error("Password minimal 8 karakter")
            elif password != confirm_password:
                st.error("Password dan konfirmasi password tidak cocok")
            else:
                user = register_user(username, password, email, full_name, address, phone)
                if user:
                    st.success("Pendaftaran berhasil! Silakan login.")
                    st.session_state.user = user
                    st.switch_page("pages/beranda.py")

def main():
    # Tampilkan navbar dari app utama
    from app import show_navbar
    show_navbar()
    
    if is_logged_in():
        show_profile()
    else:
        show_register_form()

if __name__ == "__main__":
    main()
