import streamlit as st

class SessionState:
    def __init__(self):
        self.user = st.session_state.get('user')
    
    @property
    def is_logged_in(self):
        return self.user is not None
    
    @property
    def is_admin(self):
        return self.is_logged_in and self.user.get('role') == 'admin'

def get_session_state():
    return SessionState()
