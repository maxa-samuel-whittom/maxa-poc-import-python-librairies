from typing import Any, Dict, Iterator, List, Union
import snowflake.snowpark as snowpark
from sqlfluff.core import FluffConfig, Linter

#session = snowpark.Session.builder.configs(CONNECTION_PARAMETERS).create()
#session.custom_package_usage_config = {"enabled": True}
#session.add_requirements("./environment.yml")
#session.add_packages(["sqlfluff==2.3.5"])
config = FluffConfig(
    overrides={
        "dialect": "snowflake",
        "exclude_rules": "L009",
        "library_path": "none",
    }
)

#@udf(packages=["sqlfluff"])
def lint(sql_query):
  linted_file = Linter(config=config).lint_string(sql_query)
  return linted_file.get_violations() == []
