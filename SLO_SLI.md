# Fiche SLO / SLI

| SLI (métrique)            | Méthode de mesure                | SLO cible (période)        | Objectif d'alerte |
|---------------------------|----------------------------------|----------------------------|--------------------|
| Disponibilité (200 OK)    | % de réponses 200 sur total req  | 99.5% / 30 jours           | 99.8% (warning)    |
| Latence p95               | p95 http_req_duration (k6)       | < 300 ms (période 5m/30j)  | >250 ms (warning)  |
| Taux d’erreur             | % requêtes non 200 (k6)          | < 1% / 30 jours            | >0.5% (warning)    |
| Saturation CPU            | % utilisation CPU (Prometheus)   | < 80% moyenne sur pods     | >70% (warning)     |
| Requêtes / s / pod (SLI)  | http_requests_per_second (Prom)  | >= 5 req/s/pod (HPA target)| <5 (warning)       |
