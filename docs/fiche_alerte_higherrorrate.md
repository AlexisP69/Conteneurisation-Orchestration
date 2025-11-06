# Fiche d’exploitation — Alerte HighErrorRate

## Description
Surveille le **taux d’erreurs 5xx** sur l’API `my-api`.  
Déclenchement si >2% d’erreurs pendant 10 minutes.

## Détails techniques
- Expression PromQL :
  ```promql
  sum(rate(http_requests_total{app="my-api",status=~"5.."}[5m])) / sum(rate(http_requests_total{app="my-api"}[5m])) > 0.02
  ```
- Gravité : `warning`
- Durée avant déclenchement : `10m`

## Risques associés
Un taux d’erreurs élevé indique :
- Un service backend en échec
- Une surcharge CPU ou mémoire
- Une dépendance externe non disponible

## Actions correctives
1. Vérifier les logs applicatifs (Grafana → Loki)
2. Vérifier la charge du pod et les métriques d’erreur
3. Redéployer le service si instable
4. Escalader à l’équipe backend si persistant
