import streamlit as st
from data import util

st.title("Feedback")

# Connect to the database
conn = util.get_connection()

st.subheader("Add Feedback")

# Add a row to feedback
table_name = "feedback"
columns_df = conn.query(f"PRAGMA table_info({table_name})")  # get the column info
col_values = {n: None for n in columns_df["name"].values}

for col in columns_df.itertuples():
    if col.name == 'user_id' or col.name == 'type':
        col_values[col.name] = st.text_input(f"Feedback {col.name} (type {col.type})")
    elif col.name == 'feedback':
        col_values[col.name] = st.text_area(f"Feedback {col.name} (type {col.type})")

with st.form("form"):
    submitted = st.form_submit_button("Add new row")

if submitted:
    conn._instance.execute(
        f"insert into {table_name} values ({', '.join(['?' for _ in col_values])})",
        list(col_values.values()),
    )
    row_count = conn.query(
        f"select count(1) from {table_name}",
        ttl=0,  # don't cache results
    )
    st.write(f"{table_name} now has {row_count.iat[0,0]} rows.")

st.subheader("Current Feedback")

# Read the feedback table
select_query = """
    SELECT id, user_id, type, feedback
    FROM feedback
"""
st.write(f"Query is: `{select_query}`")
result_df = conn.query(
    select_query,
    ttl=0,  # don't cache results
)
st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True,
)
