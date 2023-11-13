import streamlit as st
from snowflake.snowpark.context import get_active_session

session = get_active_session()
session.custom_package_usage_config = {"enabled": True}
session.add_packages(["sqlfluff==2.3.5"])

def lint_query(query):
    result = session.sql(f"call public.lint('{query}')").collect()
    st.success(result[0])

# Write directly to the app
st.title("Test SQL Fluff")

st.header(str(session.get_packages()))

st.button(
    "Validate Query",
    on_click=lint_query,
    args=("SELECT 1 FOMR cdi",),
)
