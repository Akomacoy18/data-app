import streamlit as st
from data import util

st.title("Manage Search")

st.warning("If you see errors, ensure you've created the table(s) first using the `Create & read` pages.")

conn = util.get_connection()
value = st.text_input("Location to search (City or Suburb)")

result_df = conn.query(
    f"""
    SELECT restaurants.name, locations.city, locations.suburb
    FROM restaurants
    JOIN locations ON restaurants.location_id = locations.id
    WHERE locations.city = :value OR locations.suburb = :value
    """,  
    params=dict(value=value),
    ttl=0,  # don't cache results so changes in the database are immediately retrieved
)
num_rows_found = len(result_df)
st.write(f'{num_rows_found} row{"" if num_rows_found == 1 else "s"} found for `{value}`')
st.dataframe(
    result_df,
    use_container_width=True,
    hide_index=True,
)
