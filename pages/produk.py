# pages/2_🛒_Produk.py
import streamlit as st
from utils.auth import is_logged_in, get_current_user
from utils.db import db

st.set_page_config(
    page_title="Produk - BelanjaIn",
    page_icon="🛒"
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

def show_products():
    st.title("Daftar Produk 🛒")
    
    # Filter produk
    col1, col2 = st.columns(2)
    with col1:
        search_query = st.text_input("Cari produk", "")
    with col2:
        categories = db.execute_query("SELECT * FROM categories", fetch_all=True)
        category_options = {c['category_id']: c['name'] for c in categories}
        selected_category = st.selectbox(
            "Kategori", 
            options=["Semua"] + list(category_options.values())
        )
    
    # Query produk
    query = "SELECT p.*, c.name as category_name FROM products p LEFT JOIN categories c ON p.category_id = c.category_id WHERE 1=1"
    params = []
    
    if search_query:
        query += " AND p.name ILIKE %s"
        params.append(f"%{search_query}%")
    
    if selected_category and selected_category != "Semua":
        category_id = [k for k, v in category_options.items() if v == selected_category][0]
        query += " AND p.category_id = %s"
        params.append(category_id)
    
    products = db.execute_query(query, params, fetch_all=True)
    
    if not products:
        st.warning("Tidak ada produk yang ditemukan.")
        return
    
    # Tampilkan produk
    cols = st.columns(3)
    for idx, product in enumerate(products):
        with cols[idx % 3]:
            st.image(product.get('image_url', 'https://via.placeholder.com/150'), width=200)
            st.subheader(product['name'])
            st.write(f"**Rp {product['price']:,.2f}**")
            st.caption(product['description'])
            st.write(f"Stok: {product['stock']}")
            st.write(f"Kategori: {product['category_name']}")
            
            if is_logged_in():
                quantity = st.number_input(
                    "Jumlah", 
                    min_value=1, 
                    max_value=product['stock'], 
                    value=1,
                    key=f"qty_{product['product_id']}"
                )
                
                if st.button("Tambah ke Keranjang", key=f"add_{product['product_id']}"):
                    user_id = get_current_user()['user_id']
                    # Cek apakah produk sudah ada di keranjang
                    existing = db.execute_query(
                        "SELECT * FROM cart WHERE user_id = %s AND product_id = %s",
                        (user_id, product['product_id']),
                        fetch_one=True
                    )
                    
                    if existing:
                        # Update quantity
                        db.execute_query(
                            "UPDATE cart SET quantity = quantity + %s WHERE cart_id = %s",
                            (quantity, existing['cart_id'])
                        )
                    else:
                        # Insert baru
                        db.execute_query(
                            "INSERT INTO cart (user_id, product_id, quantity) VALUES (%s, %s, %s)",
                            (user_id, product['product_id'], quantity)
                        )
                    
                    st.success("Produk ditambahkan ke keranjang!")
            else:
                st.warning("Login untuk menambahkan ke keranjang")

def main():
    if not is_logged_in():
        st.warning("Silakan login terlebih dahulu untuk melihat produk.")
        st.stop()
    
    show_navbar()
    show_products()

if __name__ == "__main__":
    main()
