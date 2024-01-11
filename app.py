import streamlit as st
from snowflake.snowpark.context import get_active_session

# "Back-end" import: Streamlit calls a procedure that imports sqlfluff
def lint_query_via_procedure(query):
    result = session.sql(f"CALL code_schema.lint('{query}')").collect()
    st.success(result[0])

# "Front-end" import: Streamlit imports sqlfluff itself
# I put everything in this method (like import sys), just to show
# that the "back-end method" does not it, only the "front-end method"
def lint_query_in_streamlit(session, query):
    session.custom_package_usage_config = { "enabled": True }
    session.add_requirements("./environment.yml")
    import sys
    # sqlfluff
    sys.path.append("packages/sqlfluff.zip")
    from sqlfluff.core import FluffConfig, Linter
    # snowflake-sqlalchemy
    # session.add_import("packages/snowflake_sqlalchemy-1.5.1-py2.py3-none-any.zip") # Does not work
    sys.path.append("packages/snowflake-sqlalchemy.zip")
    st.text(sys.path)
    from snowflake_sqlalchemy.snowdialect import SnowflakeDialect

    config = FluffConfig(
        overrides={
            "dialect": "snowflake",
            "exclude_rules": "L009",
            "library_path": "none",
        }
    )
    linted_file = Linter(config=config).lint_string(query)
    result = linted_file.get_violations() == []
    st.success(result)

session = get_active_session()

st.title("Test SQL Fluff")
with st.form("my_form"):
    input_val = st.text_input("Query")
    st.form_submit_button(
        "Validate Query via procedure",
        on_click=lint_query_via_procedure,
        args=(input_val,)
    )

    st.form_submit_button(
        "Validate Query in Streamlit",
        on_click=lint_query_in_streamlit,
        args=(session, input_val,)
    )
