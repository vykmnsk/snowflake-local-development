import snowflake.connector
from os import getenv, makedirs

DDL_ROOT_DIR = 'DDL'
DRYRUN = False


def get_databases_schemas():
    sql = """
SELECT db.database_name, sch.schema_name,
FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASES db
JOIN SNOWFLAKE.ACCOUNT_USAGE.SCHEMATA sch ON db.database_name = sch.catalog_name
WHERE sch.schema_name NOT IN ('INFORMATION_SCHEMA')
AND db.database_name NOT IN ('SNOWFLAKE')
AND db.database_name NOT ILIKE 'USER$%'
AND db.database_name in ('')
AND sch.schema_name in ('' ,'PUBLIC')
AND db.deleted IS NULL
AND sch.deleted IS NULL
ORDER BY 1, 2;
"""
    rows = sf.execute(sql).fetchall()
    return rows


def get_ddls_type(obj_type, db, schema):
    obj_types = obj_type.replace('_', ' ') + 'S'
    sql = f"SHOW {obj_types} in schema {db}.{schema};"
    rows = sf.execute(sql).fetchall()

    show_name_idx = 1
    if obj_type == 'SEQUENCE':
        show_name_idx = 0
    names = (row[show_name_idx] for row in rows)
    return get_ddls(obj_type, db, schema, names)


def get_ddls_type_udf(udf_type, db, schema):
    def discard_return(signature):
        return signature.split('RETURN')[0].rstrip()

    sql = f"SHOW USER {udf_type}S in schema {db}.{schema};"
    rows = sf.execute(sql).fetchall()
    names_args = (discard_return(row[8]) for row in rows)
    return get_ddls(udf_type, db, schema, names_args)


def get_ddls(obj_type, db, schema, objects):
    def enquote(obj_name, obj_type):
        if not (obj_type == 'PROCEDURE' or obj_type == 'FUNCTION'):
            return f'"{obj_name}"'
        return obj_name

    sql_lines = []
    for obj in objects:
        quoted_obj = enquote(obj, obj_type)
        sql_lines.append(
            f"SELECT '{obj}', GET_DDL('{obj_type}', '{db}.{schema}.{quoted_obj}')"
        )
    if not sql_lines:
        return []
    sql = '\nUNION\n'.join(sql_lines) + ";"
    try:
        obj_ddls = sf.execute(sql).fetchall()
    except Exception:
        print('!Error in SQL:', sql)
        raise

    return obj_ddls


func_2_obj_type_map = {
    get_ddls_type: [
        'FILE_FORMAT',
        'SEMANTIC_VIEW',
        'SEQUENCE',
        'STREAM',
        'TABLE',
        'TASK',
        'VIEW',
        ],
    get_ddls_type_udf: [
        'FUNCTION',
        'PROCEDURE',
        ]
    # STAGES get_ddl not working in Snowflake
}


def dir_name_for(obj_type: str):
    return obj_type.title() + 's'


def write_object_to_file(db, schema, obj_dir, object, ddl):
    dir_path = f'{DDL_ROOT_DIR}/{db}/{schema}/{obj_dir}'
    file_path = f'{dir_path}/{object}.sql'
    print(f'{file_path}')
    if not DRYRUN:
        makedirs(dir_path, exist_ok=True)
        with open(file_path, "w", encoding='utf-8') as file:
            file.write(ddl)


with snowflake.connector.connect(
    account=getenv('SNOWFLAKE_ACCOUNT'),
    user=getenv('SNOWFLAKE_USER'),
    password=getenv('SNOWFLAKE_PASSWORD'),
    role=getenv('SNOWFLAKE_ROLE'),
    warehouse=getenv('SNOWFLAKE_WAREHOUSE'),
).cursor() as sf:
    for db, schema in get_databases_schemas():
        print()
        print(db, '/', schema)
        print('---')

        for get_ddl_func, obj_types in func_2_obj_type_map.items():
            for obj_type in obj_types:
                obj_dir = dir_name_for(obj_type)
                print(obj_dir)
                for obj, ddl in get_ddl_func(obj_type, db, schema):
                    write_object_to_file(db, schema, obj_dir, obj, ddl)
