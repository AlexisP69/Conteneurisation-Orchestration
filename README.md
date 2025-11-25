# POC DataPress – Conteneurs & Kubernetes

Ce dépôt contient un POC complet pour l'entreprise DataPress, basé sur Docker, Kubernetes
et un début de CI/CD.

## Structure

- `app/api/` : API FastAPI minimaliste (endpoints `/` et `/health`)
- `app/front/` : Front HTML statique servi par NGINX
- `k8s/` : Manifests Kubernetes (namespace, deployments, services, configmap, secret)
- `workflows/` : Workflow CI GitHub Actions (build de l'image API)
- `docs/` : Documentation technique
- `docker-compose.yml` : Mode développement local
- `README.md` : Présent fichier

## Lancement en développement

Prérequis : Docker et Docker Compose installés.

```bash
docker compose up --build
```

- Front : http://localhost:8080
- API : http://localhost:8000/ et http://localhost:8000/health

## Déploiement sur Kubernetes

Voir `docs/README-technique.md` pour le détail :

1. Construire et pousser les images dans votre registre.
2. Appliquer les manifests dans le namespace `datapress-recette`.
3. Vérifier les pods et accéder au front via le NodePort 30080.
