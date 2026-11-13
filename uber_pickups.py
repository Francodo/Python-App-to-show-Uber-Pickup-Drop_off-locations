# Import python packages
import streamlit as st
import pandas as pd
import numpy as np
import os
from snowflake.snowpark.context import get_active_session

st.title('Python App to show Uber Pickup & Drop_off locations')

st.write(
  """In this example code for Streamlit Python application, I want to use Streamlit's core features for analyics to create an interactive app; exploring a public Uber dataset for pickups and drop-offs in New York City. This demonstration will show to fetch and cache data, draw charts, plot information on a map, and use interactive widgets, like a slider, to filter results.
  **If you're new to Streamlit:**
  check out easy-to-follow guides at
  [docs.streamlit.io](https://docs.streamlit.io).
  """
)

st.markdown("""
- :page_with_curl: [Streamlit open source documentation](https://docs.streamlit.io)
- :snowflake: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit)
- :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)
- :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)
""")

st.write(""" Here are the steps starting with data engineering:
    1. Create a database
    2. Create schema
    3. Create a stage
    4. Upload Uber data (Raw) to the stage
    5. Create a file format
    6. Create a table in the database
    7. Copy the Uber data into the table
    8. Explore the data and be familiar with column objects. 
    
    This script does use a DataFrame (pandas.DataFrame) as you will see in     the code!
    When set data = conn.query(query, ttl="1d"), Snowflake executes the        SQL query on the server and automatically packages the resulting rows      and columns into an in-memory Pandas DataFrame assigned to the             variable "data". """)


# 1. Connection and Session Setup - Initialize connection and session at the script level for Snowpark sessions. Streamlit’s native st.connection abstracts away connection pooling, secrets management (.streamlit/secrets.toml), and reconnect logic. The session = conn.session() line bridges Streamlit to Snowpark, giving you access to Snowflake’s native execution API if needed.

# conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))
# session = conn.session()

cnx = st.connection("snowflake")
session = cnx.session()

DATE_COLUMN = 'date/time'


# 2. Performance Optimization via Caching - Streamlit reruns the entire Python script from top to bottom every single time a user interacts with a widget (like clicking a checkbox or moving a slider). Without @st.cache_data, the app would re-query Snowflake on every click, causing severe latency and high cloud costs. Caching saves the DataFrame in memory for 1 day (ttl="1d").

@st.cache_data

def load_data(nrows):
    # Query your Snowflake table using the connection
    query = f'SELECT * FROM UBER_DATA.PUBLIC.uber_raw_data_sep14 LIMIT         {nrows}'
    data = conn.query(query, ttl="1d")
    
    # Convert column names to lowercase to match your DATE_COLUMN constant
    data.columns = [str(col).lower() for col in data.columns]
    
    # Data Hygiene & Standardization-Convert the date/time column to           pandas datetime objects, Databases       often return column names in      uppercase (DATE/TIME), while Python and       pandas prefer lowercase      (date/time). Explicitly normalizing column         headers and             converting raw string dates into actual Python datetime        objects     (pd.to_datetime) is vital. Without this step, time-based                   operations like .dt.hour would fail.
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    
    return data

# 3. UI Feedback States - Create a text element and let the reader know the data is loading. Large datasets take a few seconds to query and transfer. Mutating text elements (data_load_state.text) provides essential user experience (UX) feedback so users know the app hasn't frozen.
data_load_state = st.text('Loading data...')

# Load 10,000 rows of data into the dataframe.
data = load_data(10000)

# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

# 4. Conditional Rendering & Interactive Display - st.checkbox acts as a toggle gate. Rendering massive raw tables (10,000 rows) slows down the browser DOM. Using a checkbox ensures the table is rendered only when the user explicitly requests it.

if st.checkbox('Pickup & Drop_off data'):
    st.subheader('Actual Data Points')
    st.write(data)

    
# 5. Aggregations with NumPy - Let's take things a step further and draw a histogram to see what Uber's busiest hours are in New York City. Instead of writing complex SQL GROUP BY statements, this leverages Python libraries (numpy) on the Pandas DataFrame to bin timestamps into 24 hourly buckets, feeding directly into Streamlit's native st.bar_chart

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]

# To draw this diagram we used Streamlit's native bar_chart() method
st.bar_chart(hist_values)

# Let's figure out where pickups were concentrated throughout the city

st.subheader('Map of all pickups')
# Use the st.map() function to plot the data:
st.map(data)

# 6. Geospatial Mapping & Reactivity - This showcases Streamlit’s reactive execution. Moving the st.slider widget changes the hour_to_filter variable, which immediately filters the Pandas DataFrame (data[...]), re-renders the subheader, and redraws st.map(filtered_data) in real-time.
"""
 **Use the slider and watch the map update in real time.**
"""
hour_to_filter = st.slider('Hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)

# Create a line_chart using the data
st.subheader('A line chart for Number of pickups by hour')
st.line_chart(hist_values)
 









