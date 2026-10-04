import pandas as pd
import streamlit as st
from database import get_connection

def maintenance_page(user):
    st.header("Maintenance Management")
    with get_connection() as conn:
        assets = pd.read_sql_query("SELECT id,asset_code,name FROM assets ORDER BY asset_code", conn)
        records = pd.read_sql_query(
            """SELECT m.id,a.asset_code,a.name,m.issue,m.service_date,m.technician,m.cost,m.status,m.resolution
            FROM maintenance m JOIN assets a ON a.id=m.asset_id ORDER BY m.id DESC""", conn)
    st.dataframe(records, use_container_width=True, hide_index=True)

    if user["role"] not in ("Admin","Lab Technician") or assets.empty:
        return

    with st.form("maintenance"):
        label = st.selectbox("Asset", assets.apply(lambda r: f"{r.asset_code} - {r.name}", axis=1))
        issue = st.text_input("Issue / Service")
        date = st.date_input("Service date")
        technician = st.text_input("Technician")
        cost = st.number_input("Cost", min_value=0.0, step=100.0)
        status = st.selectbox("Status", ["Open","In Progress","Completed"])
        resolution = st.text_area("Resolution")
        ok = st.form_submit_button("Save record", type="primary")

    if ok:
        asset_id = int(assets.loc[assets.asset_code == label.split(" - ",1)[0], "id"].iloc[0])
        if not issue.strip():
            st.error("Issue/service is required.")
            return
        with get_connection() as conn:
            conn.execute(
                """INSERT INTO maintenance
                (asset_id,issue,service_date,technician,cost,status,resolution)
                VALUES(?,?,?,?,?,?,?)""",
                (asset_id,issue.strip(),str(date),technician.strip(),cost,status,resolution.strip()))
            if status != "Completed":
                conn.execute(
                    "UPDATE assets SET status='Under Repair',condition='Needs Repair' WHERE id=?",
                    (asset_id,))
            conn.commit()
        st.success("Maintenance record saved.")
        st.rerun()
