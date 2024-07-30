import streamlit as st
from data import util

st.title("Manage Bookings")

# Connect to the database
conn = util.get_connection()

st.subheader("Add booking")

# Add a row to bookings
table_name = "bookings"
columns_df = conn.query(f"PRAGMA table_info({table_name})")  # get the column info
col_values = {n: None for n in columns_df["name"].values}

# Get restaurant names, ids and location_ids
restaurants_df = conn.query("SELECT id, name, location_id FROM restaurants")
restaurant_names = restaurants_df['name'].values.tolist()
restaurant_ids = restaurants_df['id'].values.tolist()
restaurant_location_ids = restaurants_df['location_id'].values.tolist()

for col in columns_df.itertuples():
    if col.name == 'restaurant_id':
        selected_restaurant = st.selectbox('Select Restaurant', restaurant_names)
        col_values[col.name] = restaurant_ids[restaurant_names.index(selected_restaurant)]
        col_values['location_id'] = restaurant_location_ids[restaurant_names.index(selected_restaurant)]
    elif col.name == 'booking_date':
        col_values[col.name] = st.date_input('Select Booking Date')
    elif col.name != 'location_id':
        col_values[col.name] = st.text_input(f"Booking {col.name} (No duplicate numbers) (type {col.type})")

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


st.subheader("Current Bookings")

# Read the bookings table
select_query = """
    SELECT bookings.id, restaurants.name, locations.city, locations.suburb, bookings.booking_date
    FROM bookings
    JOIN restaurants ON bookings.restaurant_id = restaurants.id
    JOIN locations ON restaurants.location_id = locations.id
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
