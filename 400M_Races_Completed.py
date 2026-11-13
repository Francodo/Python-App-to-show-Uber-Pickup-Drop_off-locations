# Import python packages
import streamlit as st
import pandas as pd
import numpy as np
import os
from snowflake.snowpark.functions import col, when_matched

st.title('App to demonstrate how to create a Bar Graph From Dataframe')

# Write directly to the app
#st.title(f"Example Streamlit App :balloon: {st.__version__}")
st.write(
  """In this example code for Streamlit Python app, I have used a very        basic data of 400M Races Completed by an athlete to demonstrate:
  1. How to fetch data
  2. Convert raw data to  dataframe
  3. Draw charts
  4. Plot information on a Map
  5. Create widgets such as slider to filter.
  
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

# Create a database connection to Snowflake
conn = st.connection("snowflake", ttl=os.getenv("SNOWFLAKE_CONNECTION_TTL"))
session = conn.session()

# Use an interactive slider to get user input
hifives_val = st.slider(
  "Number of 400M Races completed in Q3",
  min_value=0,
  max_value=90,
  value=60,
  help="Use this to enter the number of 400M Races Completed in Q3",
)

#  Create an example dataframe
#  Note: this is just some dummy data, but you can easily connect to your Snowflake data
#  It is also possible to query data using raw SQL using session.sql() e.g. session.sql("select * from table")
created_dataframe = session.create_dataframe(
  [[50, 25, "Q1"], [20, 35, "Q2"], [hifives_val, 30, "Q3"]],
  schema=["RACES", "FIST_BUMPS", "QUARTER"],
)

# Execute the query and convert it into a Pandas dataframe
queried_data = created_dataframe.to_pandas()

# Create a simple bar chart
# See docs.streamlit.io for more types of charts
st.subheader("Number 400M Races completed")
st.bar_chart(data=queried_data, x="QUARTER", y="RACES")

st.subheader("The data for 400M Races completed graph")
st.dataframe(queried_data, use_container_width=True)
