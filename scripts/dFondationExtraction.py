from pathlib import Path
import os
import yaml

import pyodbc
from snowflake.connector import connect

###################################################################

BASE_DIR = Path(__file__).resolve().parent.parent
SCRIPT_DIR = Path(__file__).resolve().parent

# locals.yml
with open(
    BASE_DIR / "configs" / "locals.yml",
    "r",
    encoding="utf-8"
) as file:
    config = yaml.safe_load(file)

# schema.yml
with open(
    SCRIPT_DIR / "schema.yml",
    "r",
    encoding="utf-8"
) as file:
    schema_config = yaml.safe_load(file)


print("=== Snowflake ===")
print(config["snowflake"]["user_snowflake"])

print("=== SQL Server ===")
print(config["credentials"]["sql_server"])
print(config["credentials"]["database"])
print(config["credentials"]["sql_user"])

snowflake_conn = {
    "account": config["snowflake"]["account"],
    "user": config["snowflake"]["user_snowflake"],
    "password": os.getenv("DFONDATION"),
    "warehouse": config["snowflake"]["warehouse"],
    "database": config["snowflake"]["database"],
    "role": config["snowflake"]["role"],
}

sql_conn = {
    "driver": config["credentials"]["driver_odbc"],
    "server": config["credentials"]["sql_server"],
    "port": config["credentials"]["sql_port"],
    "database": config["credentials"]["database"],
    "schema": config["credentials"]["schema"],
    "user": config["credentials"]["sql_user"],
    "password": config["credentials"]["sql_password"],
}

print("=== SQL ===")
print({**sql_conn, "password": "***"})

print("=== Snowflake ===")
print({**snowflake_conn, "password": "***"})


###################################################################

cnx = pyodbc.connect(
    f"DRIVER={{{sql_conn['driver']}}};"
    f"SERVER={sql_conn['server']},{sql_conn['port']};"
    f"DATABASE={sql_conn['database']};"
    f"UID={sql_conn['user']};"
    f"PWD={sql_conn['password']};"
    "Encrypt=yes;"
    "TrustServerCertificate=yes;"
)
print("Connexion SQL Server réussie")

sf_cnx = connect(
    account=snowflake_conn["account"],
    user=snowflake_conn["user"],
    password=snowflake_conn["password"],
    warehouse=snowflake_conn["warehouse"],
    database=snowflake_conn["database"],
    role=snowflake_conn["role"],
)
print("Connexion Snowflake réussie")


###################################################################

sf_cursor = sf_cnx.cursor()
cursor = cnx.cursor()

for extract_name, conf in schema_config.items():

    print(f"Traitement : {extract_name}")

    for table_name, table_conf in conf["tables"].items():

        fields = ", ".join(table_conf["fields"])

        query = f"""
        SELECT
            {fields}
        FROM {snowflake_conn["database"]}.{conf["schema"]}.{table_name}
        """

        print(
            f"Extraction : {conf['schema']}.{table_name}"
        )

        df = (
            sf_cursor
            .execute(query)
            .fetch_pandas_all()
        )

        print(
            f"{table_name} : {len(df):,} lignes | "
            f"{len(df.columns)} colonnes"
        )

        # Suppression si la table existe
        cursor.execute(f"""
        IF OBJECT_ID('{sql_conn["schema"]}.{table_name}') IS NOT NULL
            DROP TABLE [{sql_conn["schema"]}].[{table_name}]
        """)

        # Création dynamique de la table
        columns_sql = ",\n".join(
            f"[{col}] NVARCHAR(MAX)"
            for col in df.columns
        )

        cursor.execute(f"""
        CREATE TABLE [{sql_conn["schema"]}].[{table_name}] (
        {columns_sql}
        )
        """)

        cnx.commit()

        # Préparation du INSERT
        cursor.fast_executemany = True

        placeholders = ",".join(
            ["?"] * len(df.columns)
        )

        insert_sql = f"""
        INSERT INTO [{sql_conn["schema"]}].[{table_name}]
        VALUES ({placeholders})
        """

        cursor.executemany(
            insert_sql,
            df.astype(object)
              .where(df.notna(), None)
              .values.tolist()
        )

        cnx.commit()

        print(
            f"{table_name} chargée dans SQL Server"
        )

print("Extraction terminée")

sf_cursor.close()
cursor.close()

sf_cnx.close()
cnx.close()

print("Connexions fermées")