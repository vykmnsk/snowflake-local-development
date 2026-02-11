# Create deploy execute python code in Snowflake using local dev environment


## Develop locally

### Create Python Virtual Environment [Optional]
	python3 -m venv .venv
	source .venv/bin/activate
	which python
	which pip


### Install required python app libs
	pip install -r requirements.txt


### Run locally
	python app/functions.py Fred
	python extract_ddl.py

### Unit test function(s) locally
	pip install pytest
	pytest app/tests.py


## Deploy/run on Snowflake

### Install local snowpark client
	pip install snowflake-cli-labs
	snow --version

### Setup Snowflake credentials:

#### Create config file (~/.config/snowflake/config.toml) with connection info

	snow connection add
- connection name: [sandbox]
- account = "***"
- user = "***"
- password = "***"
- role = "SANDBOX_DEVELOPER"
- warehouse = "SANDBOX_WH"
- database = "SANDBOX_DB"
- schema = "DEV"

#### Set default connection
	snow connection set-default sandbox

#### Connect and verify
	snow connection test


### Create required DB objects (one time setup)
	snow sql -f sql/setup_db.sql


### Deploy function(s) and procedure(s) to Snowflake and execute there
	snow snowpark build
	snow snowpark deploy --replace
	snow snowpark execute function "hello_function('Fred')"
	snow snowpark execute procedure "hello_procedure('Fred')"


### Test created sprocs and functions in Snowflake
	snow sql -f sql/test_db.sql
