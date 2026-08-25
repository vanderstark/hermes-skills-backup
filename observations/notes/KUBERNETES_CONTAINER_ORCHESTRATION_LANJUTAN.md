# 📦 Kubernetes & Container Orchestration: Master Pengelolaan Datacenter 170-Server

**Skill dasar:** `devops/kubernetes-operator`  
**Kategori:** Devops / Infrastruktur  
**Target:** Pengelolaan 170-server datacenter Polri  
**Bahasa:** Indonesian

---

## 🎯 Ringkasan Skill

Kubernetes memecah kelelawan pengelolaan banyak server secara manual. Dengan **Kubernetes Operator**, kita bisa:

- ✅ *Auto-healing* layanan (crash → auto restart)
- ✅ *Auto-scaling* resource (CPU/Memori naik 2x → tambahkan node)
- ✅ Zero-downtime deployment (update layanan tanpa interruption)

---

## 🔧 Alur Kerja (Design → Operasional)

### Tahap 1: Dasar-Dasar Kubernetes
```
1. Kubernetes vs Docker Swarm — K8s lebih powerful untuk skala besar
2. Master Node (kontrol) vs Worker Node (runtime)
3. Pod (satuan terkecil = satu atau lebih container)
4. Service (arahin request ke pod yang sedang DOWN)
5. Deployment (deklarasikan "ingin saya punya 3 versi service")
6. Ingress (router HTTP/HTTPS ke service internal)
```

### Tahap 2: Operator untuk Polri
Operator adalah *controller* yang mengatur lifecycle resource Kubernetes secara otomatis.

```yaml
# contoh deployment service API intelkam dari file YAML
apiVersion: apps/v1
kind: Deployment
metadata:
  name: intelkam-api
spec:
  replicas: 3   # 3 instance untuk high availability
  selector:
    matchLabels:
      app: intelkam-api
  template:
    metadata:
      labels:
        app: intelkam-api
    spec:
      containers:
      - name: intelkam-api
        image: registry.local/intelkam-api:v1.2
        ports:
        - containerPort: 8080
        env:
        - name: DB_HOST
          value: "postgres.intelligence.svc.cluster.local"
```

---

## 📋 Use Case untuk Datacenter 170-Server

| Use Case | Teknologi | Manfaat |
|---|---|---|
| Monitoring service internal | Prometheus + Grafana | Deteksi outage sebelum laporan |
| Load balancing traffic masuk | NGINX Ingress Controller | Distribusi beban ke banyak server |
| Backup & Disaster Recovery | Velero | Restore otomatis pod saat node crash |
| CI/CD Pipeline | Argo CD | Deploy otomatis feature baru ke production |

---

### Tahap 3: Komponen Penting yang Perlu Dipelajari

1.  **kubectl** — CLI utama untuk interaksi dengan cluster
2.    **Helm** — Package manager Kubernetes (seperti npm/npm untuk Docker images)
3.    **RBAC (Role-Based Access Control)** — Kontrol akses pengguna ke resource cluster
4.    **PersistentVolume (PV)** — Penyimpanan data yang stabil meski pod di-restart

---

## ⚠️ Pitfalls untuk Polri

- Jangan langsung deploy ke production 170 server. Coba dulu di *staging cluster* (bisa pakai microk8s di 1 VM)
- Resource limit (CPU/Memory) harus diketahui ya. Kalau tidak, pod *OOM-kill* sendiri
- Backup etcd (database state K8s) wajib harian via cron

---

**Status:** Siap kerja  
**Next Step:** Install `minikube` atau `kind` untuk practicum, lalu ikuti tutorial "Kubernetes the Hard Way" versi sederhana
