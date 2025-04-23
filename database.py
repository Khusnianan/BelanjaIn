import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:iguefKwACKrTVamieBDyZxcjTKNDVcEG@maglev.proxy.rlwy.net:40486/railway"
engine = create_engine(DATABASE_URL)

def get_products():
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM products")
        products = pd.DataFrame(result.fetchall(), columns=result.keys())
    return products

def add_product(name, price, category):
    with engine.connect() as connection:
        connection.execute("INSERT INTO products (name, price, category) VALUES (%s, %s, %s)", (name, price, category))

def delete_product(product_id):
    with engine.connect() as connection:
        connection.execute("DELETE FROM products WHERE id = %s", (product_id,))

def get_categories():
    with engine.connect() as connection:
        result = connection.execute("SELECT DISTINCT category FROM products")
        categories = [row[0] for row in result]
    return categories
