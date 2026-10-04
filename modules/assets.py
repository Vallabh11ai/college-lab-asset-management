import pandas as pd
import streamlit as st
from database import get_connection

CATEGORIES = ["Computer","Monitor","Projector","Printer","Networking","UPS","Keyboard/Mouse","Other"]
CONDITIONS = ["New","Good","Needs Repair","Damaged","Retired"]
STATUSES = ["Available","Assigned","Under Repair","Unavailable","Retired"]

def asset_page(user):
    st.header("Asset Management")
    view, add = st.tabs(["View Assets", "Add Asset"])

    with view:
        with get_connection() as conn:
            df = pd.read_sql_query("SELECT * FROM assets ORDER BY id DESC", conn)
        search = st.text_input("Search assets")
        category = st.selectbox("Category", ["All"] + CATEGORIES)
        filtered = df.copy()
        if search:
            mask = filtered.astype(str).apply(lambda c: c.str.contains(search, case=False, na=False))
            filtered = filtered[mask.any(axis=1)]
        if category != "All":
            filtered = filtered[filtered.category == category]
        st.dataframe(filtered, use_container_width=True, hide_index=True)

        if user["role"] in ("Admin","Lab Technician") and not filtered.empty:
            selected = st.selectbox("Select asset to update", filtered.asset_code.tolist())
            row = filtered[filtered.asset_code == selected].iloc[0]
            with st.form("update_asset"):
                condition = st.selectbox("Condition", CONDITIONS, index=CONDITIONS.index(row.condition))
                status = st.selectbox("Status", STATUSES, index=STATUSES.index(row.status))
                assigned = st.text_input("Assigned to", row.assigned_to or "")
                notes = st.text_area("Notes", row.notes or "")
                if st.form_submit_button("Update"):
                    with get_connection() as conn:
                        conn.execute(
                            "UPDATE assets SET condition=?,status=?,assigned_to=?,notes=? WHERE id=?",
                            (condition,status,assigned,notes,int(row.id)))
                        conn.commit()
                    st.success("Updated.")
                    st.rerun()

    with add:
        if user["role"] not in ("Admin","Lab Technician"):
            st.warning("Only Admin and Lab Technician can add assets.")
            return
        with st.form("add_asset"):
            code = st.text_input("Asset code")
            name = st.text_input("Asset name")
            category = st.selectbox("Category", CATEGORIES)
            lab = st.text_input("Laboratory")
            purchase = st.date_input("Purchase date")
            warranty = st.date_input("Warranty until")
            condition = st.selectbox("Condition", CONDITIONS)
            status = st.selectbox("Status", STATUSES)
            assigned = st.text_input("Assigned to")
            serial = st.text_input("Serial number")
            notes = st.text_area("Notes")
            ok = st.form_submit_button("Add Asset", type="primary")
        if ok:
            if not code.strip() or not name.strip() or not lab.strip():
                st.error("Asset code, name and laboratory are required.")
            else:
                try:
                    with get_connection() as conn:
                        conn.execute(
                            """INSERT INTO assets
                            (asset_code,name,category,laboratory,purchase_date,warranty_until,condition,status,assigned_to,serial_number,notes)
                            VALUES(?,?,?,?,?,?,?,?,?,?,?)""",
                            (code.strip(),name.strip(),category,lab,str(purchase),str(warranty),
                             condition,status,assigned.strip(),serial.strip(),notes.strip()))
                        conn.commit()
                    st.success("Asset added.")
                except Exception as e:
                    st.error(str(e))
