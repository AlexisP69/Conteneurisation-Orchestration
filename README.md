# TP Observabilité — S7

## 🎯 Objectifs

Mettre en place un **stack complet d’observabilité** dans Kubernetes :
- **Métriques** : Prometheus + Grafana  
- **Logs** : Loki + Promtail  
- **Traces distribuées** : Jaeger + OpenTelemetry  
- **Alerting** : 2 règles Prometheus documentées  
- **Dashboard Grafana** : latence, erreurs, saturation

---

## 🧱 Déploiement

### 1. Namespace
```bash
kubectl create namespace observability
```

### 2. Prometheus + Grafana
```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update
helm install monitor prometheus-community/kube-prometheus-stack -n observability --create-namespace
```

### 3. Loki + Promtail
```bash
helm repo add grafana https://grafana.github.io/helm-charts
helm repo update
helm install loki grafana/loki-stack -n observability --set promtail.enabled=true
```

### 4. Jaeger Operator
```bash
kubectl apply -n observability -f https://github.com/jaegertracing/jaeger-operator/releases/latest/download/jaeger-operator.yaml
kubectl apply -n observability -f manifests/jaeger.yaml
```

### 5. ServiceMonitor (exemple)
```bash
kubectl apply -f manifests/servicemonitor.yaml
```

### 6. Alertes Prometheus
```bash
kubectl apply -f manifests/alerts.yaml
```

---

## 📊 Dashboard Grafana

Importer le fichier :
```
dashboard/grafana-dashboard.json
```

Il contient :
- Latence 95e percentile
- Taux d’erreurs 5xx
- Saturation CPU / mémoire

---

## 🚨 Alertes Prometheus

Deux alertes configurées :
- **HighErrorRate** : plus de 2 % d’erreurs 5xx sur 10 min  
- **PodHighRestarts** : redémarrages anormaux de pods (>5 en 15 min)

Fiches associées :
- [`fiche_alerte_higherrorrate.md`](docs/fiche_alerte_higherrorrate.md)
- [`fiche_alerte_podhighrestarts.md`](docs/fiche_alerte_podhighrestarts.md)

---

## 🔍 Vérification du setup

```bash
kubectl get pods -n observability
kubectl port-forward svc/monitor-grafana 3000:80 -n observability
kubectl port-forward svc/simplest-query 16686:16686 -n observability
```

- Grafana : http://localhost:3000  
- Jaeger : http://localhost:16686
