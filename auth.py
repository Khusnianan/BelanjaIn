import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:iguefKwACKrTVamieBDyZxcjTKNDVcEG@maglev.proxy.rlwy.net:40486/railway"
engine = create_engine(DATABASE_URL)

def register_user(username, password):
    with engine.connect() as connection:
        connection.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))

def authenticate_user(username, password):
    with engine.connect() as connection:
        result = connection.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        return result.fetchone() is not None
