# Extraction_SOI

Script Python permettant l'extraction de données depuis dFondation (Snowflake) et leur chargement direct dans une base de données SQL Server.

## Fonctionnement

Le script :

1. Se connecte à dFondation (Snowflake)
2. Lit la configuration des extractions définies dans `schema.yml`
3. Extrait les données dans des DataFrames Pandas
4. Crée ou remplace les tables correspondantes dans SQL Server
5. Charge les données directement dans la base de données cible

## Prérequis

- Accès à dFondation (Snowflake)
- Accès à la base SQL Server cible
- Python 3.11+
- Poetry
- Driver ODBC SQL Server installé

## Préparation

### Environnement Python

Créer l'environnement virtuel et installer les dépendances du projet :

```bash
poetry install
```

## Configuration

### locals.yml

Compléter le fichier `configs/locals.yml` :

```yaml
snowflake:
  account:
  user_snowflake:
  warehouse:
  database:
  role:

credentials:
  driver_odbc:
  sql_server:
  sql_port:
  database:
  schema:
  sql_user:
  sql_password:
```

### Authentification Snowflake

Le script utilise l'authentification SSO configurée pour votre compte dFondation. Assurez-vous que :

- votre compte dispose des rôles requis pour accéder aux schémas configurés;
- vous êtes autorisé à accéder à l'environnement Snowflake utilisé.

Aucune génération de jeton (token) ni configuration supplémentaire n'est requise.

### schema.yml

Les schémas, tables et colonnes à extraire sont définis dans `scripts/schema.yml`.

Exemple :

```yaml
SCO:
  schema: AFFAIRES_SCOLAIRE

  tables:

    DIM_ELEVE:
      fields:
        - ELEVE_ID
        - CODE_UNIQUE_ELEVE
        - FICHE
        - CODE_PERMANENT

    DIM_ECOLE:
      fields:
        - ECOLE_ID
        - ECOLE_CODE
        - ECOLE_CODE_OFFICIEL
```

## Ajouter une nouvelle extraction

Pour ajouter une table, il suffit de modifier `schema.yml`.

Exemple :

```yaml
DIM_TEMPS:
  fields:
    - TEMPS_ID
    - ANNEE_SCOLAIRE
```

Aucune modification du code Python n'est nécessaire.

## Exécution

Lancer le script :

```bash
poetry run python scripts/dFondationExtraction.py
```

## Résultat

Pour chaque table configurée :

- les données sont extraites depuis Snowflake;
- la table cible est recréée dans SQL Server;
- les données sont chargées directement dans la base de données cible.

Aucun fichier CSV intermédiaire n'est généré.