from snowflake.connector import connect
import pandas as pd
import settings
import logging
from datetime import datetime

# Configuration du logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def extractSchema(conf: dict):

    logging.info(f"Connexion au schéma {conf['schema']} avec le rôle {conf['role']}")

    connection = connect(
        user=settings.conn["user"],
        password=settings.conn["password"],
        account=settings.conn["account"],
        warehouse=settings.conn["warehouse"],
        database=settings.conn["database"],
        schema=conf["schema"],
        role=conf["role"]
    )

    logging.info("Connexion Snowflake établie")

    cur = connection.cursor()

    try:
        for tableName, fields in conf["tables"].items():

            logging.info(f"Début extraction de la table {tableName}")

            query = f"SELECT {fields} FROM {tableName}"
            logging.debug(query)

            start_time = datetime.now()

            df = (
                cur.execute(query)
                .fetch_pandas_all()
                .replace(';', '', regex=True)
            )

            output_file = settings.pathPreFix / f"{tableName}.csv"

            df.to_csv(
                output_file,
                sep=';',
                index=False,
                header=True
            )

            duration = (datetime.now() - start_time).total_seconds()

            logging.info(
                f"Table {tableName} exportée : {len(df):,} lignes -> {output_file} ({duration:.1f}s)"
            )

    finally:
        connection.close()
        logging.info("Connexion Snowflake fermée")


logging.info("Début des extractions")

for schemaName, conf in settings.dfondation.items():

    logging.info(f"Traitement de la configuration : {schemaName}")

    try:
        extractSchema(conf)

    except Exception as e:
        logging.exception(
            f"Erreur lors de l'extraction pour la configuration {schemaName}"
        )
        continue

logging.info("Fin des extractions")