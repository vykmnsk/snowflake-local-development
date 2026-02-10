# Extract Snowflake objects DDL


## Install

### Create Python Virtual Environment [Optional]
    python -m venv .venv
    source .venv/bin/activate
    which python
    which pip

### Install required python app libs
    pip install -r requirements.txt


## Configure environment variables
    SNOWFLAKE_ACCOUNT
    SNOWFLAKE_USER
    SNOWFLAKE_PASSWORD
    SNOWFLAKE_ROLE
    SNOWFLAKE_WAREHOUSE


## Run
    python extract_ddl.py