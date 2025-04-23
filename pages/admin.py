# pages/5_⚙️_Admin.py
import streamlit as st
from utils.auth import is_logged_in, is_admin, get_current_user
from utils.db import db

st.set_page_config(
    page_title="Admin Dashboard - BelanjaIn",
    page_icon="⚙️"
)

def manage_products():
    st.subheader("Kelola Produk")
    
    # Tab untuk produk
    tab1, tab2, tab3 = st.tabs(["Daftar Produk", "Tambah Produk", "Edit Produk"])
    
    with tab1:
        products = db.execute_query("SELECT p.*, c.name as category_name FROM products p LEFT JOIN categories c ON p.category_id = c.category_id", fetch_all=True)
        if products:
            st.dataframe(products)
        else:
            st.info("Belum ada produk")
    
    with tab2:
        with st.form("add_product"):
            name = st.text_input("Nama Produk")
            description = st.text_area("Deskripsi")
            price = st.number_input("Harga", min_value=0.0, step=1000.0)
            stock = st.number_input("Stok", min_value=0, step=1)
            
            categories = db.execute_query("SELECT * FROM categories", fetch_all=True)
            category_options = {c['category_id']: c['name'] for c in categories}
            selected_category = st.selectbox(
                "Kategori", 
                options=list(category_options.values())
            )
            
            image_url = st.text_input("URL Gambar")
            
            submitted = st.form_submit_button("Tambah Produk")
            if submitted:
                category_id = [k for k, v in category_options.items() if v == selected_category][0]
                db.execute_query(
                    "INSERT INTO products (name, description, price, stock, category_id, image_url) "
                    "VALUES (%s, %s, %s, %s, %s, %s)",
                    (name, description, price, stock, category_id, image_url)
                )
                st.success("Produk berhasil ditambahkan!")
    
    with tab3:
        products = db.execute_query("SELECT * FROM products", fetch_all=True)
        if products:
            product_options = {p['product_id']: p['name'] for p in products}
            selected_product = st.selectbox(
                "Pilih Produk", 
                options=list(product_options.values())
            )
            
            product_id = [k for k, v in product_options.items() if v == selected_product][0]
            product = db.execute_query(
                "SELECT * FROM products WHERE product_id = %s",
                (product_id,),
                fetch_one=True
            )
            
            with st.form("edit_product"):
                name = st.text_input("Nama Produk", value=product['name'])
                description = st.text_area("Deskripsi", value=product['description'])
                price = st.number_input("Harga", min_value=0.0, step=1000.0, value=float(product['price']))
                stock = st.number_input("Stok", min_value=0, step=1, value=product['stock'])
                
                categories = db.execute_query("SELECT * FROM categories", fetch_all=True)
                category_options = {c['category_id']: c['name'] for c in categories}
                selected_category = st.selectbox(
                    "Kategori", 
                    options=list(category_options.values()),
                    index=[k for k, v in category_options.items() if k == product['category_id']][0]
                )
                
                image_url = st.text_input("URL Gambar", value=product.get('image_url', ''))
                
                submitted = st.form_submit_button("Update Produk")
                if submitted:
                    category_id = [k for k, v in category_options.items() if v == selected_category][0]
                    db.execute_query(
                        "UPDATE products SET name = %s, description = %s, price = %s, stock = %s, "
                        "category_id = %s, image_url = %s, updated_at = CURRENT_TIMESTAMP "
                        "WHERE product_id = %s",
                        (name, description, price, stock, category_id, image_url, product_id)
                    )
                    st.success("Produk berhasil diupdate!")
        else:
            st.info("Belum ada produk untuk diedit")

def manage_orders():
    st.subheader("Kelola Pesanan")
    
    status_options = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    selected_status = st.selectbox("Filter Status", options=["Semua"] + status_options)
    
    query = "SELECT o.*, u.username FROM orders o JOIN users u ON o.user_id = u.user_id"
    params = []
    
    if selected_status != "Semua":
        query += " WHERE o.status = %s"
        params.append(selected_status)
    
    orders = db.execute_query(query, params, fetch_all=True)
    
    if orders:
        for order in orders:
            with st.expander(f"Order #{order['order_id']} - {order['status']}"):
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"**Pelanggan:** {order['username']}")
                    st.write(f"**Total:** Rp {order['total_amount']:,.2f}")
                    st.write(f"**Metode Pembayaran:** {order['payment_method']}")
                with col2:
                    st.write(f"**Alamat Pengiriman:** {order['shipping_address']}")
                    st.write(f"**Tanggal Pesan:** {order['created_at']}")
                
                # Order items
                items = db.execute_query(
                    "SELECT oi.*, p.name FROM order_items oi JOIN products p ON oi.product_id = p.product_id "
                    "WHERE oi.order_id = %s",
                    (order['order_id'],),
                    fetch_all=True
                )
                
                st.write("**Item Pesanan:**")
                for item in items:
                    st.write(f"- {item['name']} x{item['quantity']} @Rp {item['price']:,.2f}")
                
                # Update status
                new_status = st.selectbox(
                    "Ubah Status",
                    options=status_options,
                    index=status_options.index(order['status']),
                    key=f"status_{order['order_id']}"
                )
                
                if st.button("Update Status", key=f"update_{order['order_id']}"):
                    db.execute_query(
                        "UPDATE orders SET status = %s, updated_at = CURRENT_TIMESTAMP WHERE order_id = %s",
                        (new_status, order['order_id'])
                    )
                    st.experimental_rerun()
    else:
        st.info("Tidak ada pesanan")

def manage_users():
    st.subheader("Kelola Pengguna")
    
    users = db.execute_query("SELECT * FROM users", fetch_all=True)
    
    if users:
        st.dataframe(users)
    else:
        st.info("Belum ada pengguna")

def main():
    if not is_logged_in():
        st.warning("Silakan login terlebih dahulu.")
        st.stop()
    
    if not is_admin():
        st.error("Anda tidak memiliki akses ke halaman ini.")
        st.stop()
    
    st.title("Admin Dashboard ⚙️")
    
    tab1, tab2, tab3 = st.tabs(["Produk", "Pesanan", "Pengguna"])
    
    with tab1:
        manage_products()
    
    with tab2:
        manage_orders()
    
    with tab3:
        manage_users()

if __name__ == "__main__":
    main()
