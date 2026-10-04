import streamlit as st
from database import get_connection, hash_password

def login_ui():
    with st.form("login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        ok = st.form_submit_button("Login", type="primary")
    if ok:
        with get_connection() as conn:
            row = conn.execute(
                "SELECT id,username,full_name,role FROM users WHERE username=? AND password_hash=?",
                (username.strip(), hash_password(password))).fetchone()
        if row:
            st.session_state.user = dict(row)
            st.rerun()
        else:
            st.error("Invalid username or password.")
    with st.expander("Demo accounts"):
        st.write("Admin: admin / admin123")
        st.write("Technician: technician / tech123")
        st.write("Student: student / student123")

def logout():
    st.session_state.user = None
