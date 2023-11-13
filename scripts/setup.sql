-- Setup script for the Hello Snowflake! application.
CREATE APPLICATION ROLE app_public;
CREATE SCHEMA IF NOT EXISTS core;
GRANT USAGE ON SCHEMA core TO APPLICATION ROLE app_public;

-- Schema CodeSchema
CREATE OR ALTER VERSIONED SCHEMA code_schema;
GRANT USAGE ON SCHEMA code_schema TO APPLICATION ROLE app_public;

-- UDFs
-- pytest, tblib, importlib_resources, etc... are dependencies of sqlfluff
CREATE or REPLACE FUNCTION code_schema.lint(query string)
  RETURNS boolean
  LANGUAGE PYTHON
  RUNTIME_VERSION=3.8
  IMPORTS = ('/python/query_validator.py', '/packages/sqlfluff-2.3.5-py3-none-any.zip')
  PACKAGES=('snowflake-snowpark-python', 'pytest', 'tblib', 'importlib_resources', 'appdirs', 'toml', 'tqdm', 'jinja2', 'regex', 'pathspec', 'chardet')
  HANDLER='query_validator.lint';

GRANT USAGE ON FUNCTION code_schema.lint(STRING) TO APPLICATION ROLE app_public;

-- Streamlit App
CREATE STREAMLIT code_schema.test_sqlfluff_streamlit
  FROM '/streamlit'
  MAIN_FILE = '/app.py';

GRANT USAGE ON STREAMLIT code_schema.test_sqlfluff_streamlit TO APPLICATION ROLE app_public;
