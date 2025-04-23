# utils/db.py
import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
import os

class Database:
    def __init__(self):
        self.conn = None
        self.connect()
        
    def connect(self):
        try:
            self.conn = psycopg2.connect(
                database="railway",
                user="postgres",
                password="iguefKwACKrTVamieBDyZxcjTKNDVcEG",
                host="maglev.proxy.rlwy.net",
                port="40486"
            )
            print("Database connected successfully")
        except Exception as e:
            print(f"Database connection error: {e}")
    
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        try:
            if not self.conn or self.conn.closed:
                self.connect()
                
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                
                if fetch_one:
                    result = cursor.fetchone()
                elif fetch_all:
                    result = cursor.fetchall()
                else:
                    self.conn.commit()
                    result = None
                    
                return result
                
        except Exception as e:
            print(f"Query execution error: {e}")
            self.conn.rollback()
            return None
    
    def close(self):
        if self.conn:
            self.conn.close()

# Initialize database
db = Database()

# Create tables if not exists
def init_db():
    queries = [
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            full_name VARCHAR(100),
            address TEXT,
            phone VARCHAR(20),
            role VARCHAR(20) DEFAULT 'customer',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS categories (
            category_id SERIAL PRIMARY KEY,
            name VARCHAR(50) UNIQUE NOT NULL,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            price DECIMAL(10, 2) NOT NULL,
            stock INTEGER NOT NULL,
            category_id INTEGER REFERENCES categories(category_id),
            image_url VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            total_amount DECIMAL(10, 2) NOT NULL,
            status VARCHAR(20) DEFAULT 'pending',
            shipping_address TEXT NOT NULL,
            payment_method VARCHAR(50) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS order_items (
            order_item_id SERIAL PRIMARY KEY,
            order_id INTEGER REFERENCES orders(order_id),
            product_id INTEGER REFERENCES products(product_id),
            quantity INTEGER NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS cart (
            cart_id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(user_id),
            product_id INTEGER REFERENCES products(product_id),
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, product_id)
        )
        """
    ]
    
    for query in queries:
        db.execute_query(query)
    
    # Insert admin user if not exists
    db.execute_query(
        "INSERT INTO users (username, password, email, full_name, role) "
        "VALUES (%s, %s, %s, %s, %s) "
        "ON CONFLICT (username) DO NOTHING",
        ("admin", "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", "admin@belanja.in", "Admin BelanjaIn", "admin")
    )

init_db()
