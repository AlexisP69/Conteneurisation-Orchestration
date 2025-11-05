# TP S6 — Scalabilité & Résilience

## Objectifs
- Dimensionner via requests/limits & QoS
- Mettre en œuvre HPA (CPU + métrique externe req/s)
- Gérer la résilience avec PDB
- Pratiquer un déploiement Canary via Argo Rollouts
- Mesurer les performances avec k6 (SLO/SLI)

## Contenu du dossier
- `deployment-api.yaml` : Déploiement et service httpbin
- `hpa-api.yaml` : HPA (CPU + métrique Pods)
- `pdb-api.yaml` : PodDisruptionBudget
- `rollout-api-canary.yaml` : Déploiement Canary (bonus)
- `k6-rps.js` : Script de charge k6
- `SLO_SLI.md` : Fiche SLO/SLI remplie

## Utilisation rapide

```bash
kubectl create ns workshop
kubectl apply -f deployment-api.yaml
kubectl apply -f pdb-api.yaml
kubectl apply -f hpa-api.yaml
# (Optionnel) Canary
kubectl delete deployment api -n workshop --ignore-not-found
kubectl apply -f rollout-api-canary.yaml
```

Lancer le test de charge :
```bash
kubectl port-forward svc/api 8080:80 -n workshop &
k6 run k6-rps.js
```

Exporter les résultats :
```bash
k6 run --out json=results.json k6-rps.js
```
