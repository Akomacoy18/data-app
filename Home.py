import streamlit as st
from data import util

st.set_page_config(
    page_title="KAI.FY",
)

st.header("KAI.FY")

st.subheader("Welcome to KAI.FY")
st.write("This is the dataapp prototype for KAI.FY")
st.info("Tick the box and click run to get started")
st.write("\n")





import streamlit as st
from data import util

st.title("Create and Read a table")


conn = util.get_connection()
# We use a form to control when the page is (re)loaded and hence when the data is reset or retrieved.
with st.form("form"):
    should_reset = st.checkbox("(Re)create database with tables?")
    submitted = st.form_submit_button("Run")

if submitted:
    if should_reset:
        for table_name in util.VALID_TABLE_NAMES:
            util.reset_table(conn, table_name)

