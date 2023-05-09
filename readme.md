## Api ERP

# Projet API de génération de QR Code

Le projet est une API construite avec FastAPI pour générer des QR Codes à partir des informations d'identification de l'utilisateur, envoyer les QR Codes par e-mail et effectuer diverses opérations sur les produits.

## Structure du projet

Le projet est structuré de la manière suivante :

api.py: Le fichier principal contenant l'application FastAPI et les points de terminaison.
secure.py: Contient les fonctions liées à la sécurité, comme la création de jetons JWT et la vérification des mots de passe.
qr_code.py: Contient la fonction pour générer un code QR.
mail.py: Contient la fonction pour envoyer un e-mail avec une pièce jointe (le code QR).
db.py: Contient les fonctions pour interagir avec la base de données.
test_api.py: Contient les tests unitaires pour l'API.
ci.yaml: Configure le pipeline d'intégration continue et de déploiement continu (CI/CD) avec GitHub Actions.
requirements.txt: Liste toutes les dépendances nécessaires pour exécuter l'application.
Procfile: Utilisé par Heroku pour déterminer comment démarrer l'application.
runtime.py: Indique la version Python à utiliser pour exécuter l'application.

## Fonctionnalités

Générer des codes QR à partir des informations d'identification de l'utilisateur.
Envoyer des codes QR par e-mail aux utilisateurs.
Récupérer des données sur les produits à partir d'une API externe.
Rechercher des produits par nom ou par prix.
Protéger les points de terminaison avec des jetons JWT.

## Points de terminaison

Voici les points de terminaison disponibles dans l'API :

/ (GET): Renvoie un message "Hello World".
/send_qr (POST): Génère un code QR à partir des informations d'identification de l'utilisateur et l'envoie par e-mail.
/products (GET): Récupère les données des produits à partir d'une API externe.
/validate-token (GET): Valide un jeton JWT.
/products/{product_id} (GET): Récupère les données d'un produit spécifique à partir d'une API externe.
/products/search/{name}{price} (GET): Recherche des produits par nom ou par prix.

## Tests

Les tests unitaires pour l'API se trouvent dans le fichier test_api.py. Ils utilisent le module unittest et la classe TestClient de FastAPI pour tester les points de terminaison.

## Intégration continue et déploiement continu (CI/CD)

Le fichier ci.yaml configure le pipeline d'intégration continue et de déploiement continu (CI/CD) avec GitHub Actions. Le pipeline exécute les tests unitaires et déploie l'application sur Heroku si les tests réussissent.

## Dépendances

Le fichier requirements.txt liste toutes les dépendances nécessaires pour exécuter l'application. Pour installer ces dépendances, exécutez pip install -r requirements.txt.

## Déploiement sur Heroku

Le fichier Procfile est utilisé par Heroku pour déterminer comment démarrer l'application. Le fichier runtime.py indique la version Python à utiliser pour exécut
