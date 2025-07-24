import streamlit as st
import pandas as pd
import snowflake.connector

st.set_page_config(page_title="Student Dashboard", layout="wide")
st.title("🎓 Student Data Analytics")

# Connect to Snowflake
conn = snowflake.connector.connect(
    user=st.secrets["SNOWFLAKE_USER"],
    password=st.secrets["SNOWFLAKE_PASSWORD"],
    account=st.secrets["SNOWFLAKE_ACCOUNT"],
    warehouse=st.secrets["SNOWFLAKE_WAREHOUSE"],
    database=st.secrets["SNOWFLAKE_DATABASE"],
    schema=st.secrets["SNOWFLAKE_SCHEMA"]
)

query1 = "SELECT Major, COUNT(*) AS student_count FROM cleaned_data GROUP BY Major ORDER BY student_count DESC"
df1 = pd.read_sql(query1, conn)
st.subheader("📊 Student Count by Major")
st.bar_chart(df1.set_index("Major"))


# Enrollment Status Summary
query2 = "SELECT Enrollment_Status, COUNT(*) AS count FROM cleaned_data GROUP BY Enrollment_Status"
df2 = pd.read_sql(query2, conn)
st.subheader("👨‍🎓 Enrollment Status")
st.dataframe(df2)

# Filter by Country
st.subheader("🌎 Students by Country")
countries = pd.read_sql("SELECT DISTINCT Country FROM cleaned_data", conn)["Country"]
selected = st.selectbox("Select Country", countries)
filtered = pd.read_sql(f"SELECT * FROM cleaned_data WHERE Country = '{selected}'", conn)
st.dataframe(filtered)
