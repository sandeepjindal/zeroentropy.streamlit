# streamlit_app.py

import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np

[theme]
base="dark"
primaryColor="purple"

# Initialize connection.
# Uses st.cache_resource to only run once.
@st.cache_resource
def init_connection():
    return snowflake.connector.connect(
        **st.secrets["snowflake"], client_session_keep_alive=True
    )

conn = init_connection()


# Perform query.
# Uses st.cache_data to only rerun when the query changes or after 10 min.
@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

rows = run_query("SELECT * from carboncredit;")

st.header("Demo in 1 day :joy:")
st.subheader("Powered by Snowpark for Python and Snowflake Data Marketplace | Made with Streamlit")

# Print results.
for row in rows:
    st.write(f"{row[0]} has a :{row[1]}:")
    

