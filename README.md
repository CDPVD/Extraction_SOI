# Extraction_SOI
Script python permettant l'extraction des données du SOI dans dFondation

## Préparation
-Utiliser Poetry pour vous créer un environnement de développement et y installer les dépendances du projet
-Aller sur https://app.snowflake.com/grics/dfondation/#/homepage
    |--> Dans Governance & Security --> Users & roles --> trouver votre utilisateur
        |--> Cliquer sur Generate token (Programmatic access tokens), remplir le forms et choisir __All of this user's roles__ ce sera important pour pouvoir changer de role "on the fly" pendant l'extraction de différent schéma

## Config
Dans configs.py:
    1-Changer le chemin où écrire la SEED
    2-Le user et la clef d'environnement pour l'accès

## Ajouter d'autres tables
Vous pouvez ajouter d'autre table à extraire de dFondation en respectant la structure de la config:

"Nom de l'extraction" : {
        "role": "Role requis pour l'accès",
        "schema": "Schéma de dFondation",
        "tables": {
            "Nom de la table" : "Colonne voulu",
            "Nom de la table 2 du même schéma au besoin" : "..."  
        }
    }

## Lancer le script
Simplement lancer le script pour tester votre configuration.