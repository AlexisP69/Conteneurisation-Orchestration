# TP S4 Kubernetes - Workshop

## Objectif
Déployer un front Nginx et une API httpbin sur Kubernetes avec Ingress et TLS sur `workshop.local`.

## Prérequis
- Minikube installé
- Ingress-nginx installé
- Cert-manager installé
- Accès GHCR si vous utilisez l’image `ghcr.io/nginxdemos/hello:plain-text`

## Installation

1. Créer le namespace et les ressources :

```bash
kubectl apply -f tp-s4.yaml
```
2. Vérifier que les pods sont Running :

```bash
kubectl get pods -n workshop
```
3. Si vous utilisez GHCR, créer le secret Docker pour l’authentification :

```bash
kubectl create secret docker-registry ghcr-creds \
  --docker-server=ghcr.io \
  --docker-username=<github-username> \
  --docker-password=<personal-access-token> \
  --docker-email=<email> \
  -n workshop
```
4. Redéployer les images :

```bash
kubectl -n workshop set image deployment/front front=ghcr.io/nginxdemos/hello:plain-text
kubectl -n workshop set image deployment/api api=kennethreitz/httpbin:latest
kubectl -n workshop rollout restart deployment/front
kubectl -n workshop rollout restart deployment/api
```
5. Tester l’accès via Ingress :

```bash
curl -k -H "Host: workshop.local" https://<minikube-ip>/front
curl -k -H "Host: workshop.local" https://<minikube-ip>/api/get
```

ConfigMap et Secrets
- front-config : contient la variable BANNER_TEXT pour le front Nginx.
- app-secrets : contient les secrets éventuels pour les applications (API).

TLS
- Le certificat TLS est auto-signé par ClusterIssuer selfsigned pour workshop.local.
- L’Ingress est configuré pour utiliser ce certificat.
