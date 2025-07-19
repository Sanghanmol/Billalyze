import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

st.set_page_config(page_title="Receipt Dashboard", layout="wide")
st.title("📄 Receipt & Bill Dashboard")

conn = conn = sqlite3.connect("F:/Billalyze/receipts.db")
df = pd.read_sql_query("SELECT * FROM receipts", conn)

if df.empty:
    st.info("No receipts found. Upload some data through the backend.")
else:
    st.subheader("📋 Uploaded Receipts")
    st.dataframe(df)

    st.subheader("📊 Spend per Vendor")
    bar_fig = px.bar(
        df, x="vendor", y="amount", title="Total Spend per Vendor", color="vendor"
    )
    st.plotly_chart(bar_fig)

    st.subheader("📈 Monthly Spend Trend")
    df["date"] = pd.to_datetime(df["date"])
    monthly = df.groupby(df["date"].dt.to_period("M"))["amount"].sum().reset_index()
    monthly["date"] = monthly["date"].astype(str)
    line_fig = px.line(
        monthly, x="date", y="amount", markers=True, title="Monthly Spend"
    )
    st.plotly_chart(line_fig)

    st.subheader("📌 Spend by Category")
    pie_df = df.groupby("category")["amount"].sum().reset_index()
    pie_fig = px.pie(
        pie_df, values="amount", names="category", title="Spend by Category"
    )
    st.plotly_chart(pie_fig)
