-- USE ROLE SANDBOX_DEVELOPER;
-- USE DATABASE SANDBOX_DB;
-- USE WAREHOUSE SANDBOX_WH;
-- USE SCHEMA DEV;


CREATE or replace TABLE testtable(FIELD1 VARCHAR);
insert into testtable(field1) values ('Fred');
insert into testtable(field1) values ('Fred again');
select * from testtable;

-- after function is created:
select hello_function(field1) from testtable;
call hello_procedure('Fred');
