# pages/1_🏠_Beranda.py
import streamlit as st
from utils.auth import is_logged_in, get_current_user
from utils.db import db

st.set_page_config(
    page_title="Beranda - BelanjaIn",
    page_icon="🏠",
    layout="wide"
)

hide_sidebar_style = """
    <style>
        section[data-testid="stSidebar"] {
            display: none !important;
        }
    </style>
"""
st.markdown(hide_sidebar_style, unsafe_allow_html=True)

def show_navbar():
    from app import show_navbar
    show_navbar()

def show_featured_products():
    st.subheader("Produk Unggulan")
    products = db.execute_query(
        "SELECT p.*, c.name as category_name FROM products p LEFT JOIN categories c ON p.category_id = c.category_id LIMIT 6",
        fetch_all=True
    )
    
    if products:
        cols = st.columns(3)
        for idx, product in enumerate(products):
            with cols[idx % 3]:
                st.image(product.get('image_url', 'https://via.placeholder.com/150'), width=200)
                st.subheader(product['name'])
                st.write(f"**Rp {product['price']:,.2f}**")
                st.caption(product['description'])
                st.write(f"Stok: {product['stock']}")
                
                if is_logged_in():
                    if st.button("Lihat Detail", key=f"view_{product['product_id']}"):
                        st.switch_page("pages/2_🛒_Produk.py")
    else:
        st.warning("Belum ada produk unggulan")

def main():
    if not is_logged_in():
        st.warning("Silakan login terlebih dahulu.")
        st.switch_page("app.py")
    
    show_navbar()
    
    user = get_current_user()
    st.title(f"Halo, {user['full_name']}!")
    st.markdown(f"Selamat datang kembali di BelanjaIn. Ada yang bisa kami bantu hari ini?")
    
    show_featured_products()

if __name__ == "__main__":
    main()
