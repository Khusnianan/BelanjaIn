import streamlit as st

def add_to_cart(product_id, name, price):
    cart = st.session_state.get("cart", {})
    if product_id in cart:
        cart[product_id]["quantity"] += 1
    else:
        cart[product_id] = {"name": name, "price": price, "quantity": 1}
    st.session_state["cart"] = cart

def view_cart():
    st.subheader("Keranjang Belanja")
    cart = st.session_state.get("cart", {})
    total = 0

    for item_id, item in cart.items():
        st.write(f"{item['name']} x {item['quantity']} = Rp{item['price'] * item['quantity']}")
        total += item['price'] * item['quantity']

    st.write("Total: Rp", total)

def clear_cart():
    st.session_state["cart"] = {}
