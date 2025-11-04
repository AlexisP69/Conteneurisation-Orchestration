# 🗃️ S5 — Persistance & Workloads avec État

## 🎯 Objectifs pédagogiques
- Comprendre le modèle de **persistance Kubernetes** : PV / PVC / StorageClass  
- Déployer une base **PostgreSQL** en **StatefulSet** avec **PVC dynamiques**  
- Mettre en place une stratégie de **sauvegarde / restauration** (backup logique avec `pg_dump` et option Velero)  

---

## 📦 Architecture du déploiement

### 🔹 Ressources déployées
| Type | Nom | Description |
|------|-----|--------------|
| Namespace | `workshop` | Espace isolé du TP |
| Secret | `pg-secret` | Contient le mot de passe `POSTGRES_PASSWORD` |
| Service | `postgres` | Service **headless** (ClusterIP=None) pour la découverte DNS |
| StatefulSet | `postgres` | Gère un pod PostgreSQL avec PVC dynamique |
| PVC | `data-postgres-0` | Volume persistant de 8 Gi (classe `standard`) |

### 🔹 Arborescence
```
.
├── 00-namespace.yaml
├── 01-secret.yaml
├── 02-service.yaml
├── 03-statefulset.yaml
└── runbook.md
```

---

## 🚀 Déploiement

### 1️⃣ Lancer le cluster Minikube
```bash
minikube start
```

### 2️⃣ Appliquer les manifests
```bash
kubectl apply -f 00-namespace.yaml
kubectl apply -f 01-secret.yaml
kubectl apply -f 02-service.yaml
kubectl apply -f 03-statefulset.yaml
```

### 3️⃣ Vérifier les ressources
```bash
kubectl -n workshop get all
kubectl -n workshop get pvc
```

> Le PVC `data-postgres-0` doit être en statut **Bound** et le pod `postgres-0` en **Running**.

---

## 🧠 Concepts clés

### 🧩 PV / PVC / StorageClass
- **PV (PersistentVolume)** : ressource de stockage réelle.
- **PVC (PersistentVolumeClaim)** : demande d’un PV.
- **StorageClass** : modèle de provisioning dynamique.
- **ReclaimPolicy** : définit le comportement du PV après suppression du PVC (`Delete` ou `Retain`).

### 🏗️ StatefulSet
- Fournit une **identité stable** aux pods (`postgres-0`, `postgres-1`, …).  
- Utilise `volumeClaimTemplates` pour créer automatiquement un PVC par pod.  
- Fonctionne avec un **Headless Service** pour la résolution DNS directe :  
  Exemple → `postgres-0.postgres.workshop.svc.cluster.local`

---

## 💾 Runbook — Backup / Restore

### 🔹 Sauvegarde logique (pg_dumpall)
```bash
POD=$(kubectl -n workshop get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}')
kubectl -n workshop exec -it "$POD" -- bash -lc 'pg_dumpall -U postgres' > backup-$(date +%F).sql
```
Crée un fichier `backup-YYYY-MM-DD.sql` contenant l’intégralité des bases PostgreSQL.

---

### 🔹 Restauration
```bash
kubectl -n workshop exec -i "$POD" -- bash -lc 'psql -U postgres' < backup-YYYY-MM-DD.sql
```

---

## ☁️ Option : Backup avec Velero
Pour aller plus loin :
```bash
velero backup create workshop --include-namespaces workshop --wait --default-volumes-to-restic
velero restore create --from-backup workshop
```

> Cette option permet de sauvegarder les objets Kubernetes **et les volumes persistants** (avec Restic).

---

## ✅ Vérification du déploiement
```bash
kubectl -n workshop exec -it postgres-0 -- psql -U postgres
```

Dans le shell PostgreSQL :
```sql
\l   -- liste des bases
\q   -- quitter
```

## 👤 Auteur
**Nom :** Alexis  
**Environnement :** Minikube (v1.34.0) sous VMware  
**Date :** Novembre 2025  
