# streamlit_app.py

import streamlit as st
import snowflake.connector
import pandas as pd
import numpy as np
from PIL import Image

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
    
chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["a", "b", "c"])

st.bar_chart(chart_data)

df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(df)

st.metric(label="Total carbon emmision cost", value=40000, delta=-0.5,
    delta_color="inverse")

st.metric(label="Fossil fuel", value=123, delta=123,
    delta_color="off")

image = Image.open('sunrise.jpeg')

st.image(image, caption='Sunrise by the mountains')
