import streamlit as st
from data import util

st.title("Payment")

# Connect to the database
conn = util.get_connection()

# Add a row to payment_info
st.subheader("Add payment_info")
table_name = "payment_info"
columns_df = conn.query(f"PRAGMA table_info({table_name})")  # get the column info
col_values = {n: None for n in columns_df["name"].values}
credit_card_details = {}

for col in columns_df.itertuples():
    if col.name == 'user_id':
        col_values[col.name] = st.text_input(f"Payment Info {col.name} (No duplicate numbers) (type {col.type})")
    elif col.name == 'payment_method':
        col_values[col.name] = st.selectbox('Select Payment Method', ['Credit Card', 'Internet Banking'])
        if col_values[col.name] == 'Credit Card':
            credit_card_details['user_id'] = col_values['user_id']
            credit_card_details['card_number'] = st.text_input("Enter Credit Card Number")
            credit_card_details['expiry_date'] = st.date_input("Enter Expiry Date")
            credit_card_details['cvv'] = st.text_input("Enter CVV")
    elif col.name == 'automatic_payments':
        col_values[col.name] = st.checkbox('Automatic Payments')

with st.form("form1"):
    submitted1 = st.form_submit_button("Add new row to payment_info")

if submitted1:
    conn._instance.execute(
        f"insert into {table_name} values ({', '.join(['?' for _ in col_values])})",
        list(col_values.values()),
    )
    row_count = conn.query(
        f"select count(1) from {table_name}",
        ttl=0,  # don't cache results
    )
    st.write(f"{table_name} now has {row_count.iat[0,0]} rows.")

    # If payment method is Credit Card, save the details to the credit_card table
    if col_values['payment_method'] == 'Credit Card':
        table_name = "credit_card"
        conn._instance.execute(
            f"insert into {table_name} values ({', '.join(['?' for _ in credit_card_details])})",
            list(credit_card_details.values()),
        )
        row_count = conn.query(
            f"select count(1) from {table_name}",
            ttl=0,  # don't cache results
        )
        st.write(f"{table_name} now has {row_count.iat[0,0]} rows.")

# Display the payment_info table
st.subheader("Current Payment Info")
result_df = conn.query(
    "SELECT * FROM payment_info",
    ttl=0,  # don't cache results
)
st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True,
)

# Display the credit_card table
st.subheader("Current Credit Card Info")
result_df = conn.query(
    "SELECT * FROM credit_card",
    ttl=0,  # don't cache results
)
st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True,
)


