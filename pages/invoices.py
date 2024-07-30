import streamlit as st
from data import util

st.title("Invoicing")

# Connect to the database
conn = util.get_connection()

# Fetch or set credit limits
st.subheader("Set Credit Limits")
credit_id = st.text_input('Enter a credit ID')
credit_limit_df = conn.query(f'SELECT "limit" FROM credit_limits WHERE id = "{credit_id}"')
if not credit_limit_df.empty:
    credit_limit = credit_limit_df.iat[0,0]
else:
    st.write("No credit limit found for the given ID.")
    new_limit = st.number_input('Enter a new credit limit')
    if st.button('Add new credit limit'):
        conn._instance.execute(
            f'INSERT INTO credit_limits (id, "limit") VALUES (?, ?)',
            (credit_id, new_limit)
        )
        st.write(f"New credit limit added for ID {credit_id}.")

# Display the credit_limits table
st.subheader("Current Credit Limits")
credit_limits_df = conn.query(
    "SELECT * FROM credit_limits",
    ttl=0,  # don't cache results
)
st.dataframe(
    credit_limits_df,
    use_container_width=True,
    hide_index=True,
)

# Add a row to invoicing
st.subheader("Add invoicing")
table_name = "invoicing"
columns_df = conn.query(f"PRAGMA table_info({table_name})")  # get the column info
col_values = {n: None for n in columns_df["name"].values}

for col in columns_df.itertuples():
    if col.name == 'id':
        col_values[col.name] = st.text_input(f"Invoicing {col.name} (No duplicate numbers) (type {col.type})")
    elif col.name == 'status':
        col_values[col.name] = st.selectbox('Select Status', ['Paid', 'Unpaid'])
    elif col.name == 'credit_limit':
        col_values[col.name] = credit_limit

with st.form("form2"):
    submitted2 = st.form_submit_button("Add new row to invoicing")

if submitted2:
    conn._instance.execute(
        f"insert into {table_name} values ({', '.join(['?' for _ in col_values])})",
        list(col_values.values()),
    )
    row_count = conn.query(
        f"select count(1) from {table_name}",
        ttl=0,  # don't cache results
    )
    st.write(f"{table_name} now has {row_count.iat[0,0]} rows.")

# Display the invoicing table
st.subheader("Current Invoices")
result_df = conn.query(
    "SELECT * FROM invoicing",
    ttl=0,  # don't cache results
)
st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True,
)
