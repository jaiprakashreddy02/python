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

# Load full table (excluding sensitive columns)
query_full = """
SELECT FANID, FIRST_NAME, LAST_NAME, MAJOR, COUNTRY, ENROLLMENT_STATUS, GRADUATED_YEAR
FROM cleaned_data
"""
df = pd.read_sql(query_full, conn)

# KPIs
total_students = df.shape[0]
unique_countries = df["COUNTRY"].nunique()
unique_majors = df["MAJOR"].nunique()
unique_years = df["GRADUATED_YEAR"].nunique()

col1, col2, col3, col4 = st.columns(4)
col1.metric("👨‍🎓 Total Students", total_students)
col2.metric("🌍 Countries", unique_countries)
col3.metric("📚 Majors", unique_majors)
col4.metric("🎓 Grad Years", unique_years)

st.markdown("---")

# Filters
st.sidebar.header("🔍 Filters")
selected_major = st.sidebar.selectbox("Filter by Major", ["All"] + sorted(df["MAJOR"].dropna().unique()))
selected_year = st.sidebar.selectbox("Filter by Graduated Year", ["All"] + sorted(df["GRADUATED_YEAR"].dropna().unique()))

filtered_df = df.copy()
if selected_major != "All":
    filtered_df = filtered_df[filtered_df["MAJOR"] == selected_major]
if selected_year != "All":
    filtered_df = filtered_df[filtered_df["GRADUATED_YEAR"] == selected_year]

# Display Filtered Table
st.subheader("📋 Filtered Student Records")
st.dataframe(filtered_df)

# Visualization 1: Student Count by Major
query1 = "SELECT MAJOR, COUNT(*) AS student_count FROM cleaned_data GROUP BY MAJOR ORDER BY student_count DESC"
df1 = pd.read_sql(query1, conn)
st.subheader("📊 Student Count by Major")
if "MAJOR" in df1.columns:
    st.bar_chart(df1.set_index("MAJOR"))

# Visualization 2: Enrollment Status Breakdown
query2 = "SELECT ENROLLMENT_STATUS, COUNT(*) AS count FROM cleaned_data GROUP BY ENROLLMENT_STATUS"
df2 = pd.read_sql(query2, conn)
st.subheader("👨‍🏫 Enrollment Status Breakdown")
st.bar_chart(df2.set_index("ENROLLMENT_STATUS"))

# Visualization 3: Students by Country
query3 = "SELECT COUNTRY, COUNT(*) AS count FROM cleaned_data GROUP BY COUNTRY ORDER BY count DESC"
df3 = pd.read_sql(query3, conn)
st.subheader("🌎 Students by Country")
st.bar_chart(df3.set_index("COUNTRY"))

# Visualization 4: Graduation Year Trend
query4 = "SELECT GRADUATED_YEAR, COUNT(*) AS count FROM cleaned_data GROUP BY GRADUATED_YEAR ORDER BY GRADUATED_YEAR"
df4 = pd.read_sql(query4, conn)
st.subheader("📈 Graduation Year Trend")
st.line_chart(df4.set_index("GRADUATED_YEAR"))
