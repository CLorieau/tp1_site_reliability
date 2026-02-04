# TP Site Reliability - Application Web Full Stack

Ce projet est une application web composée de trois services :
- **Frontend** : Interface utilisateur pour gérer les tâches
- **Backend** : API REST pour la gestion des données
- **Base de données** : PostgreSQL

## Lancement de l'application

Pour démarrer l'ensemble des services, Docker et Docker Compose doivent être installés. 
Exécutez la commande suivante à la racine du projet :

```bash
docker compose up --build
```

Cette commande va construire les images et démarrer les conteneurs en arrière-plan.

## Accès à l'application

Une fois les services démarrés, vous pouvez accéder à :

- **L'interface utilisateur (Frontend)** :
  [http://localhost:3000](http://localhost:3000)

- **La documentation de l'API (Backend)** :
  [http://localhost:8000/docs](http://localhost:8000/docs)
  (Interface Swagger UI interactive pour tester les endpoints)

## Docker Hub

Les images Docker de ce projet sont disponibles sur Docker Hub :

- **Backend** : [drashaax/tp1_site_reliability-backend](https://hub.docker.com/r/drashaax/tp1_site_reliability-backend)
- **Frontend** : [drashaax/tp1_site_reliability-frontend](https://hub.docker.com/r/drashaax/tp1_site_reliability-frontend)

Pour pousser les images sur Docker Hub :

```bash
docker compose push
```
