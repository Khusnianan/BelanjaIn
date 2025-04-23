import streamlit as st

# KONFIGURASI HALAMAN (HARUS DI AWAL)
st.set_page_config(
    page_title="Profil | BelanjaIn",
    page_icon="👤", 
    layout="wide"
)

from utils.auth_utils import is_logged_in, get_current_user, register_user
from utils.db import db
from utils.navigation import tampilkan_navbar

# Sembunyikan sidebar
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

def tampilkan_profil():
    """Halaman profil pengguna"""
    pengguna = get_current_user()
    
    st.title("Profil Saya 👤")
    
    with st.form("form_profil"):
        kolom1, kolom2 = st.columns(2)
        
        with kolom1:
            st.text_input("Username", value=pengguna['username'], disabled=True)
            email = st.text_input("Email*", value=pengguna['email'])
        
        with kolom2:
            nama_lengkap = st.text_input("Nama Lengkap*", value=pengguna['full_name'])
            telepon = st.text_input("Nomor Telepon", value=pengguna.get('phone', ''))
        
        alamat = st.text_area("Alamat", value=pengguna.get('address', ''))
        
        if st.form_submit_button("Simpan Perubahan"):
            if not (email and nama_lengkap):
                st.error("Harap isi field wajib (*)")
            else:
                db.execute_query(
                    "UPDATE users SET email = %s, full_name = %s, address = %s, phone = %s WHERE user_id = %s",
                    (email, nama_lengkap, alamat, telepon, pengguna['user_id'])
                )
                st.success("Profil berhasil diperbarui!")
                st.rerun()

def tampilkan_form_daftar():
    """Form pendaftaran pengguna baru"""
    st.title("Daftar Akun Baru 📝")
    
    with st.form("form_daftar"):
        kolom1, kolom2 = st.columns(2)
        
        with kolom1:
            username = st.text_input("Username*", help="Minimal 5 karakter")
            password = st.text_input("Password*", type="password", help="Minimal 8 karakter")
            konfirmasi_password = st.text_input("Konfirmasi Password*", type="password")
        
        with kolom2:
            email = st.text_input("Email*", help="Gunakan email aktif")
            nama_lengkap = st.text_input("Nama Lengkap*")
        
        alamat = st.text_area("Alamat")
        telepon = st.text_input("Nomor Telepon")
        
        if st.form_submit_button("Daftar Sekarang"):
            # Validasi input
            if not all([username, password, konfirmasi_password, email, nama_lengkap]):
                st.error("Harap isi semua field wajib (*)")
            elif len(username) < 5:
                st.error("Username minimal 5 karakter")
            elif len(password) < 8:
                st.error("Password minimal 8 karakter")
            elif password != konfirmasi_password:
                st.error("Password dan konfirmasi password tidak cocok")
            else:
                pengguna = register_user(username, password, email, nama_lengkap, alamat, telepon)
                if pengguna:
                    st.success("Pendaftaran berhasil! Silakan login.")
                    st.session_state.user = pengguna
                    st.switch_page("pages/beranda.py")

def main():
    # Tampilkan navbar
    tampilkan_navbar()
    
    # Tampilkan konten sesuai status login
    if is_logged_in():
        tampilkan_profil()
    else:
        tampilkan_form_daftar()

if __name__ == "__main__":
    main()
