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

# Query 1: Student Count by Major
query1 = "SELECT Major, COUNT(*) AS student_count FROM cleaned_data GROUP BY Major ORDER BY student_count DESC"
df1 = pd.read_sql(query1, conn)

# Debugging support - show actual column names
st.write("✅ Columns in df1:", df1.columns.tolist())
st.subheader("📊 Student Count by Major")

# Safely try to render bar chart
if "MAJOR" in map(str.upper, df1.columns):
    st.bar_chart(df1.set_index(df1.columns[0]))
else:
    st.warning("⚠️ 'Major' column not found in query results.")

# Query 2: Enrollment Status Summary
query2 = "SELECT Enrollment_Status, COUNT(*) AS count FROM cleaned_data GROUP BY Enrollment_Status"
df2 = pd.read_sql(query2, conn)
st.subheader("👨‍🎓 Enrollment Status")
st.dataframe(df2)

# Filter by Country
st.subheader("🌎 Students by Country")

# Run query and display the returned columns
countries_df = pd.read_sql("SELECT DISTINCT * FROM cleaned_data", conn)
st.write("Columns returned from Snowflake:", countries_df.columns.tolist())

# Check if 'COUNTRY' column exists
if "COUNTRY" in countries_df.columns:
    countries = countries_df["COUNTRY"].dropna().unique().tolist()
    selected = st.selectbox("Select Country", countries)
    filtered = pd.read_sql(f"SELECT * FROM cleaned_data WHERE COUNTRY = '{selected}'", conn)
    st.dataframe(filtered)
else:
    st.error("❌ 'COUNTRY' column not found in cleaned_data table. Please check the table schema.")
