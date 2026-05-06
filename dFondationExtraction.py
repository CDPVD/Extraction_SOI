from snowflake.connector import connect
import pandas as pd
import configs

def extractSchema(conf: dict):
        connection = connect(
            user=configs.conn["user"],
            password=configs.conn["password"],
            account=configs.conn["account"],
            warehouse=configs.conn["warehouse"],
            database=configs.conn["database"],
            schema=conf["schema"],
            role=conf["role"]
        )

        cur = connection.cursor()
        
        for tableName, fields in conf["tables"].items():
            cur.execute("SELECT " + fields + " FROM " + tableName).fetch_pandas_all().replace(';','',regex=True).to_csv(configs.pathPreFix + tableName + ".csv", sep=';', index=False, header=True)
        
        connection.close()



for schemaName, conf in configs.dfondation.items():
    try:
        extractSchema(conf)
    except Exception as e:
        print("Erreur lors de la création de la connection ou lors de l'extraction des données avec la configuration:")
        print(conf)
        print(e)
        continue