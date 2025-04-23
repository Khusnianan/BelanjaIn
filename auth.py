import streamlit as st
import hashlib
from db import get_user

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def login_user(username, password):
    user = get_user(username)
    if user and user["password"] == hash_password(password):
        return user
    return None
