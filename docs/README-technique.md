# Documentation technique – POC DataPress

## 1. Résumé du contexte

DataPress dispose aujourd'hui d'une plateforme mono-serveur regroupant front, API, base de données
et scripts. Le serveur arrive en fin de vie et les mises à jour sont risquées (coupure globale,
absence d'environnement de test dédié). Le DSI souhaite un POC basé sur Docker, Kubernetes et un début
de CI/CD afin de préparer une future modernisation.

## 2. Architecture proposée

### 2.1. Mode développement – Docker / Compose

En développement, l'environnement est lancé avec Docker Compose :

- 1 service `api` (FastAPI, port 8000) ;
- 1 service `front` (NGINX + HTML statique, port 80 exposé en 8080 sur l'hôte) ;
- un réseau `datapress-net` permettant au front de joindre l'API.

L'API expose les endpoints :

- `/` : JSON simple avec nom du service, environnement et timestamp ;
- `/health` : endpoint utilisé pour les vérifications (healthcheck/probes).

Le développeur lance simplement :

```bash
docker compose up --build
```

puis accède au front sur http://localhost:8080 et à l'API directement sur http://localhost:8000.

### 2.2. Mode recette – Kubernetes

Sur Kubernetes, nous déployons dans le namespace `datapress-recette` :

- un Deployment `datapress-api` (2 réplicas, probes HTTP sur `/health`) ;
- un Service `datapress-api` de type ClusterIP (port 80 vers 8000) ;
- un Deployment `datapress-front` (1 réplique) ;
- un Service `datapress-front` de type NodePort (port 80 exposé en 30080).

Le front communique avec l'API via le Service `datapress-api` (nom DNS `datapress-api.datapress-recette.svc.cluster.local`
ou via une configuration adaptée), ce qui découple les adresses IP.

## 3. Décisions techniques importantes

- **Docker multi-stage** pour l'API : une image de build et une image runtime plus légère.
- **Utilisateur non-root** dans le conteneur API.
- **Probes Kubernetes** :
  - `readinessProbe` HTTP GET sur `/health` ;
  - `livenessProbe` HTTP GET sur `/health`.
- **Ressources** : `requests` et `limits` mémoire positionnés sur l'API.
- **ConfigMap & Secret** :
  - `ConfigMap` `datapress-config` (WELCOME_MESSAGE, DP_ENV) ;
  - `Secret` `datapress-secret` (clé API_FAKE_TOKEN encodée en base64) ;
  - montés sous forme de variables d'environnement dans le conteneur API.

## 4. Guide d'exploitation

### 4.1. Mode développement

1. Prérequis : Docker / Docker Compose installés.
2. Cloner le dépôt.
3. Lancer :

   ```bash
   docker compose up --build
   ```

4. Vérifier :
   - front : http://localhost:8080
   - API : http://localhost:8000/ et http://localhost:8000/health

### 4.2. Déploiement Kubernetes

1. Se connecter au cluster Kubernetes.
2. Construire et publier les images (à adapter selon votre registre) :

   ```bash
   docker build -t <votre-registre>/datapress-api:latest ./app/api
   docker build -t <votre-registre>/datapress-front:latest ./app/front
   docker push <votre-registre>/datapress-api:latest
   docker push <votre-registre>/datapress-front:latest
   ```

3. Mettre à jour les champs `image` dans les manifests Kubernetes si nécessaire.
4. Appliquer les manifests :

   ```bash
   kubectl apply -f k8s/namespace.yaml
   kubectl apply -f k8s/configmap.yaml
   kubectl apply -f k8s/secret.yaml
   kubectl apply -f k8s/api-deployment.yaml
   kubectl apply -f k8s/api-service.yaml
   kubectl apply -f k8s/front-deployment.yaml
   kubectl apply -f k8s/front-service.yaml
   ```

5. Vérifications :

   ```bash
   kubectl get all -n datapress-recette
   kubectl get events -n datapress-recette --sort-by=.lastTimestamp
   kubectl logs -n datapress-recette deploy/datapress-api
   ```

6. Accès au front via NodePort (sur un nœud du cluster) :

   ```text
   http://<IP-node>:30080
   ```

## 5. Limites et pistes d'amélioration

- Pas de TLS ni d'Ingress configuré pour l'instant.
- Pas d'autoscaling ni de règles NetworkPolicy.
- Pas de monitoring avancé (Prometheus/Grafana).
- La base de données n'est pas intégrée dans ce POC minimal.

Pistes pour aller plus loin :

- Ajouter un Ingress avec TLS (certificats Let's Encrypt).
- Mettre en place un HorizontalPodAutoscaler pour l'API.
- Ajouter des dashboards de supervision et des alertes.
- Introduire une vraie base de données et des migrations.
