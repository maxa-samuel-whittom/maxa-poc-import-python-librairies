import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()
# session.custom_package_usage_config = {"enabled": True}
# session.add_packages(["sqlfluff==2.3.5"])

def lint_query(query):
    result = session.sql(f"CALL code_schema.lint('{query}')").collect()
    st.success(result[0])

# Write directly to the app
st.title("Test SQL Fluff")

with st.form("my_form"):
    input_val = st.text_input("Query")
    st.form_submit_button(
        "Validate Query",
        on_click=lint_query,
        args=(input_val,)
    )
