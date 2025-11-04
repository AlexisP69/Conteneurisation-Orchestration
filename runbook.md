# 🧰 Runbook — PostgreSQL StatefulSet (Backup & Restore)

## 📌 Objectif
Ce document décrit les étapes pratiques pour :
- Vérifier le bon fonctionnement de PostgreSQL dans Kubernetes  
- Réaliser une **sauvegarde logique** (`pg_dumpall`)  
- Restaurer une sauvegarde  
- (Optionnel) Effectuer un **backup complet avec Velero**

---

## 🔎 Vérification du déploiement

### 1️⃣ Vérifier le pod et le PVC
```bash
kubectl -n workshop get pods,pvc
```
Attendez que le pod soit en état **Running** et le PVC en **Bound** :
```
NAME          READY   STATUS    RESTARTS   AGE
postgres-0    1/1     Running   0          2m

NAME               STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   AGE
data-postgres-0    Bound    pvc-xxxxxx                                 8Gi        RWO            standard       2m
```

### 2️⃣ Tester la connexion PostgreSQL
```bash
kubectl -n workshop exec -it postgres-0 -- psql -U postgres
```
Dans le prompt `psql`, vérifier :
```sql
\l    -- liste les bases
\conninfo   -- affiche les infos de connexion
\q    -- quitter
```

---

## 💾 Sauvegarde logique (pg_dumpall)

### 1️⃣ Identifier le pod
```bash
POD=$(kubectl -n workshop get pod -l app=postgres -o jsonpath='{.items[0].metadata.name}')
echo $POD
```

### 2️⃣ Exécuter la sauvegarde
```bash
kubectl -n workshop exec -it "$POD" -- bash -lc 'pg_dumpall -U postgres' > backup-$(date +%F).sql
```
👉 Cette commande crée un fichier local `backup-YYYY-MM-DD.sql` contenant la structure et les données de toutes les bases PostgreSQL.

### 3️⃣ Vérifier la taille et le contenu
```bash
ls -lh backup-*.sql
head -20 backup-*.sql
```

---

## 🔄 Restauration

### 1️⃣ Copier ou générer le fichier de backup à restaurer
Assurez-vous d’avoir un fichier de type `backup-YYYY-MM-DD.sql`.

### 2️⃣ Exécuter la restauration
```bash
kubectl -n workshop exec -i "$POD" -- bash -lc 'psql -U postgres' < backup-YYYY-MM-DD.sql
```

### 3️⃣ Vérifier la restauration
```bash
kubectl -n workshop exec -it "$POD" -- psql -U postgres -c "\l"
```
Vous devriez retrouver vos bases restaurées.

---

## ☁️ Option : Backup & Restore avec Velero

### 1️⃣ Créer un backup complet du namespace
```bash
velero backup create workshop --include-namespaces workshop --wait --default-volumes-to-restic
```

### 2️⃣ Lister les backups
```bash
velero get backups
```

### 3️⃣ Restaurer à partir du backup
```bash
velero restore create --from-backup workshop
```

> 💡 Cette approche sauvegarde les **objets Kubernetes (YAML)** et les **volumes persistants** via Restic.

---

## 🧹 Nettoyage (facultatif)
Si vous souhaitez repartir de zéro :
```bash
kubectl delete ns workshop
```

---

## 📘 Références
- [Documentation PostgreSQL](https://www.postgresql.org/docs/)
- [Kubernetes Persistent Volumes](https://kubernetes.io/docs/concepts/storage/persistent-volumes/)
- [Velero - Official Docs](https://velero.io/docs/)

---

## 👤 Auteur
**Nom :** Alexis  
**TP :** S5 — Persistance & Workloads avec État  
**Date :** Novembre 2025  
