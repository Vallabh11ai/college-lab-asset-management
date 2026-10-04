import streamlit as st
from database import init_db, seed_demo_data
from modules.auth import login_ui, logout
from modules.assets import asset_page
from modules.maintenance import maintenance_page
from modules.complaints import complaints_page
from modules.reports import reports_page

st.set_page_config(page_title="College Lab Asset Management", page_icon="🧪", layout="wide")
init_db()
seed_demo_data()

if "user" not in st.session_state:
    st.session_state.user = None

if st.session_state.user is None:
    st.title("🧪 College Laboratory Asset Management System")
    st.caption("Python + Streamlit + SQLite")
    login_ui()
    st.stop()

user = st.session_state.user
with st.sidebar:
    st.title("Lab Asset Manager")
    st.write(f"**User:** {user['full_name']}")
    st.write(f"**Role:** {user['role']}")
    page = st.radio("Navigation", ["Dashboard", "Assets", "Maintenance", "Complaints", "Reports"])
    if st.button("Logout"):
        logout()
        st.rerun()

if page == "Dashboard":
    reports_page(True)
elif page == "Assets":
    asset_page(user)
elif page == "Maintenance":
    maintenance_page(user)
elif page == "Complaints":
    complaints_page(user)
else:
    reports_page(False)
