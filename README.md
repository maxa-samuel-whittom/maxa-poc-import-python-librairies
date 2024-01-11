This is a small project to show how you can use a Python library that's not in Snowflake's Anaconda channel.
Reference I've used [here](https://medium.com/snowflake/introducing-simple-workflow-for-using-python-packages-in-snowpark-928f667ff1aa)

(Zipping a non-=supported Python package)[https://community.snowflake.com/s/article/Importing-3rd-party-Python-packages-containing-non-Python-files-using-Snowflake-stages-when-creating-Python-UDFs]

## Running the project

In Snowsight, open a new worksheet.

Run the following commands in the worksheet:
```
USE ROLE apps_admin;
CREATE OR REPLACE DATABASE test_sqlfluff_db;
USE DATABASE test_sqlfluff_db;
CREATE SCHEMA test_sqlfluff_schema;
USE SCHEMA test_sqlfluff_schema;

CREATE OR REPLACE STAGE test_sqlfluff_stage DIRECTORY = ( ENABLE = true );
```

On your local machine, run the following command to upload the files to your newly-created Snowflake stage:
```
snowsql -c CONNECTION_NAME -f upload.sql
```

Go back to your Snowsight worksheet and run these commands:
```
DROP APPLICATION PACKAGE IF EXISTS test_sqlfluff_package;
DROP APPLICATION IF EXISTS test_sqlfluff;

CREATE APPLICATION PACKAGE test_sqlfluff_package;
USE APPLICATION PACKAGE test_sqlfluff_package;

ALTER APPLICATION PACKAGE test_sqlfluff_package
  ADD VERSION "v1_0"
  USING @test_sqlfluff_db.test_sqlfluff_schema.test_sqlfluff_stage;

CREATE APPLICATION IF NOT EXISTS test_sqlfluff
  FROM APPLICATION PACKAGE test_sqlfluff_package
  USING VERSION "v1_0";

USE APPLICATION test_sqlfluff;
```

You can then test that SQLFluff works by running these commands in the worksheet:
```
CALL code_schema.lint('SELECT 1 FROM myvalidquery'); -- returns TRUE

CALL code_schema.lint('SELLECT 1 FROMM myinvalidquery'); -- returns FALSE
```

## About This Solution

Not ideal. It works, but requires to:

- Download the .whl file of the package you want to import (and rename its extension to **.zip**). As you can see with my example, I have downloaded sqlfluff 2.3.5 and put it in the **packages** folder.
- Put most of your package's dependencies in the **PACKAGES** parameter of your UDF. See **setup.sql**. This is why this solution is not great: I was lucky that sqlfluff has only about 10 dependencies and that they were all supported by Snowflake, but this might not be the case for all libraries that we may want to import.
