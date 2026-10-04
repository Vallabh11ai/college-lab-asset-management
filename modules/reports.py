import pandas as pd
import plotly.express as px
import streamlit as st
from database import get_connection

def reports_page(dashboard_only=False):
    with get_connection() as conn:
        assets = pd.read_sql_query("SELECT * FROM assets", conn)
        maintenance = pd.read_sql_query("SELECT * FROM maintenance", conn)
        complaints = pd.read_sql_query("SELECT * FROM complaints", conn)

    st.header("Dashboard" if dashboard_only else "Reports & Analytics")
    a,b,c,d = st.columns(4)
    a.metric("Total Assets", len(assets))
    b.metric("Available", int((assets.status=="Available").sum()) if not assets.empty else 0)
    c.metric("Under Repair", int((assets.status=="Under Repair").sum()) if not assets.empty else 0)
    d.metric("Open Complaints", int((complaints.status=="Open").sum()) if not complaints.empty else 0)

    if not assets.empty:
        x,y = st.columns(2)
        cat = assets.category.value_counts().reset_index()
        cat.columns = ["Category","Count"]
        x.plotly_chart(
            px.bar(cat,x="Category",y="Count",title="Assets by Category"),
            use_container_width=True)
        stat = assets.status.value_counts().reset_index()
        stat.columns = ["Status","Count"]
        y.plotly_chart(
            px.pie(stat,names="Status",values="Count",title="Asset Status"),
            use_container_width=True)

    if not dashboard_only:
        st.subheader("Maintenance")
        total = maintenance.cost.sum() if not maintenance.empty else 0
        st.metric("Total Maintenance Cost", f"₹{total:,.2f}")
        st.dataframe(maintenance, use_container_width=True, hide_index=True)
        st.subheader("Complaints")
        st.dataframe(complaints, use_container_width=True, hide_index=True)
