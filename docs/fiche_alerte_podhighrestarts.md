# Fiche d’exploitation — Alerte PodHighRestarts

## Description
Détecte des **redémarrages anormaux** de pods Kubernetes pour l’application `my-api`.  
Déclenchement si >5 redémarrages en 15 minutes.

## Détails techniques
- Expression PromQL :
  ```promql
  increase(kube_pod_container_status_restarts_total{app="my-api"}[10m]) > 5
  ```
- Gravité : `warning`
- Durée avant déclenchement : `15m`

## Risques associés
- CrashLoopBackOff d’un container
- Problème d’environnement ou de dépendance
- Fuite mémoire, OOM kill, ou panic

## Actions correctives
1. Inspecter les logs du pod (`kubectl logs`)
2. Vérifier les ressources CPU/mémoire
3. Analyser les événements (`kubectl describe pod`)
4. Appliquer correctif ou redéploiement
