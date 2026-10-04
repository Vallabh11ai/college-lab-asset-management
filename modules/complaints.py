import pandas as pd
import streamlit as st
from database import get_connection

def complaints_page(user):
    st.header("Damage / Complaint Management")
    with get_connection() as conn:
        df = pd.read_sql_query(
            """SELECT c.id,c.reported_by,c.category,c.description,c.priority,c.status,c.created_at,a.asset_code
            FROM complaints c LEFT JOIN assets a ON a.id=c.asset_id ORDER BY c.id DESC""", conn)
        assets = pd.read_sql_query(
            "SELECT id,asset_code,name FROM assets ORDER BY asset_code", conn)

    st.dataframe(df, use_container_width=True, hide_index=True)

    with st.form("complaint"):
        choices = ["General / No specific asset"] + (
            assets.apply(lambda r: f"{r.id} - {r.asset_code} - {r.name}", axis=1).tolist()
            if not assets.empty else [])
        asset = st.selectbox("Asset", choices)
        category = st.selectbox(
            "Category",
            ["Electrical","Hardware","Network","Furniture","Software","Cleaning","Other"])
        description = st.text_area("Description")
        priority = st.selectbox("Priority", ["High","Medium","Low"])
        ok = st.form_submit_button("Submit complaint", type="primary")

    if ok:
        if not description.strip():
            st.error("Description is required.")
            return
        asset_id = None if asset.startswith("General") else int(asset.split(" - ",1)[0])
        with get_connection() as conn:
            conn.execute(
                "INSERT INTO complaints(asset_id,reported_by,category,description,priority) VALUES(?,?,?,?,?)",
                (asset_id,user["username"],category,description.strip(),priority))
            conn.commit()
        st.success("Complaint submitted.")
        st.rerun()

    if user["role"] in ("Admin","Lab Technician") and not df.empty:
        selected = st.selectbox("Complaint ID", df.id.tolist())
        statuses = ["Open","In Progress","Resolved","Closed"]
        new_status = st.selectbox("Status", statuses)
        if st.button("Update complaint"):
            with get_connection() as conn:
                conn.execute(
                    "UPDATE complaints SET status=? WHERE id=?",
                    (new_status,int(selected)))
                conn.commit()
            st.rerun()
