PUT file://./environment.yml @test_sqlfluff_package.stage_content.test_sqlfluff_stage overwrite=true auto_compress=false;
PUT file://./manifest.yml @test_sqlfluff_package.stage_content.test_sqlfluff_stage overwrite=true auto_compress=false;
PUT file://./README.md @test_sqlfluff_package.stage_content.test_sqlfluff_stage overwrite=true auto_compress=false;

PUT file://./packages/* @test_sqlfluff_package.stage_content.test_sqlfluff_stage/packages overwrite=true auto_compress=false;
PUT file://./python/query_validator.py @test_sqlfluff_package.stage_content.test_sqlfluff_stage/python overwrite=true auto_compress=false;
PUT file://./scripts/setup.sql @test_sqlfluff_package.stage_content.test_sqlfluff_stage/scripts overwrite=true auto_compress=false;
PUT file://./app.py @test_sqlfluff_package.stage_content.test_sqlfluff_stage overwrite=true auto_compress=false;
