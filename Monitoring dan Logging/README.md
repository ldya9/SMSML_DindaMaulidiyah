# Monitoring dan Logging - Kriteria 4

Sistem monitoring dan logging untuk model machine learning menggunakan Prometheus dan Grafana.

## 📁 Struktur Folder

```
Monitoring dan Logging/
├── 1.bukti_serving/                    # Screenshot bukti serving model
├── 2.prometheus.yml                    # Konfigurasi Prometheus
├── 3.prometheus_exporter.py            # Script untuk export metrics ke Prometheus
├── 4.bukti monitoring Prometheus/     # Screenshot monitoring Prometheus
│   ├── 1.monitoring_http_requests_total.png
│   ├── 2.monitoring_system_cpu_usage.png
│   ├── 3.monitoring_system_ram_usage.png
│   ├── 4.monitoring_api_latency.png
│   └── 5.monitoring_throughput.png
├── 5.bukti monitoring Grafana/        # Screenshot monitoring Grafana
│   ├── 1.monitoring_http_requests_total.png
│   ├── 2.monitoring_system_cpu_usage.png
│   ├── 3.monitoring_system_ram_usage.png
│   ├── 4.monitoring_api_latency.png
│   └── 5.monitoring_throughput.png
├── 6.bukti alerting Grafana/          # Screenshot alerting Grafana
│   ├── 1.rules_cpu_usage.png
│   ├── 2.notifikasi_cpu_usage.png
│   ├── 3.rules_ram_usage.png
│   └── 4.notifikasi_ram_usage.png
├── 7.inference.py                     # Script untuk testing inference
├── serve_model.py                     # Script untuk serving model MLflow
└── README.md                          # File ini
```

## 🚀 Setup dan Instalasi

### 1. Install Dependencies

```bash
pip install prometheus-client flask psutil requests mlflow
```

### 2. Install Prometheus

**Windows:**
1. Download dari: https://prometheus.io/download/
2. Extract dan jalankan `prometheus.exe`

**Linux/Mac:**
```bash
# Download dan extract
wget https://github.com/prometheus/prometheus/releases/download/v2.45.0/prometheus-2.45.0.linux-amd64.tar.gz
tar xvfz prometheus-2.45.0.linux-amd64.tar.gz
cd prometheus-2.45.0.linux-amd64
```

### 3. Install Grafana

**Windows:**
1. Download dari: https://grafana.com/grafana/download
2. Install dan jalankan Grafana

**Linux/Mac:**
```bash
# Ubuntu/Debian
sudo apt-get install -y software-properties-common
sudo add-apt-repository "deb https://packages.grafana.com/oss/deb stable main"
sudo apt-get update
sudo apt-get install grafana

# Start Grafana
sudo systemctl start grafana-server
sudo systemctl enable grafana-server
```

## 📝 Cara Menjalankan

### Step 1: Start MLflow Tracking Server (jika belum)

```bash
mlflow ui --port 5000
```

### Step 2: Serve Model menggunakan MLflow

**Option A: Menggunakan serve_model.py**
```bash
# Otomatis mencari latest model
python serve_model.py

# Atau specify model URI
python serve_model.py --model-uri runs:/<run_id>/model --port 5002
```

**Option B: Langsung menggunakan MLflow CLI**
```bash
mlflow models serve -m "runs:/<run_id>/model" --port 5002 --no-conda
```

### Step 3: Start Prometheus Exporter

```bash
# Set environment variable untuk model URI (jika perlu)
export MLFLOW_MODEL_URI="runs:/<run_id>/model"

# Start exporter
python prometheus_exporter.py
```

Exporter akan:
- Menjalankan Prometheus metrics server di port **8000** (http://127.0.0.1:8000/metrics)
- Menjalankan Flask inference endpoint di port **5001** (http://127.0.0.1:5001/predict)

### Step 4: Start Prometheus

```bash
# Di folder prometheus
./prometheus --config.file=../Monitoring dan Logging/prometheus.yml
```

Atau jika prometheus.yml ada di folder prometheus:
```bash
./prometheus --config.file=prometheus.yml
```

Prometheus akan berjalan di: http://127.0.0.1:9090

### Step 5: Start Grafana

**Windows:** Buka aplikasi Grafana
**Linux:** 
```bash
sudo systemctl start grafana-server
```

Grafana akan berjalan di: http://127.0.0.1:3000
- Default username: `admin`
- Default password: `admin`

### Step 6: Setup Grafana Dashboard

1. **Add Prometheus Data Source:**
   - Login ke Grafana (http://127.0.0.1:3000)
   - Configuration → Data Sources → Add data source
   - Pilih Prometheus
   - URL: `http://localhost:9090`
   - Save & Test

2. **Create Dashboard:**
   - Dashboards → New Dashboard
   - **PENTING:** Nama dashboard harus berisi username Dicoding Anda
     - Contoh: `dashboard-dindamaulidiyah` atau `dashboard-ldya9`
   - Add panels untuk metrics:
     - `http_requests_total`
     - `system_cpu_usage`
     - `system_ram_usage`
     - `api_latency_seconds`
     - `throughput_per_minute`

3. **Create Alerting (untuk Skilled):**
   - Alerting → Alert rules → New alert rule
   - Buat alert untuk CPU atau RAM usage
   - Set threshold (contoh: CPU > 80%)
   - Save

### Step 7: Generate Metrics dengan Inference

```bash
# Di terminal terpisah
python inference.py
```

Script ini akan:
- Mengirim request ke inference endpoint
- Generate metrics di Prometheus
- Update metrics secara real-time

## 📊 Metrics yang Tersedia

### 1. `http_requests_total`
- **Type:** Counter
- **Description:** Total jumlah HTTP requests
- **Labels:** method, endpoint, status

### 2. `api_latency_seconds`
- **Type:** Histogram
- **Description:** Latensi API dalam detik
- **Labels:** endpoint

### 3. `throughput_per_minute`
- **Type:** Gauge
- **Description:** Jumlah request per menit

### 4. `system_cpu_usage`
- **Type:** Gauge
- **Description:** Penggunaan CPU sistem (persentase)
- **Labels:** instance, job

### 5. `system_ram_usage`
- **Type:** Gauge
- **Description:** Penggunaan RAM sistem (persentase)
- **Labels:** instance, job

### 6. `api_model_requests_total`
- **Type:** Gauge
- **Description:** Total jumlah request API model

## 🎯 Checklist Kriteria 4

### Basic (2 pts)
- [x] Serving model menggunakan MLflow
- [x] Monitoring Prometheus dengan minimal 3 metriks berbeda
- [x] Monitoring Grafana dengan metriks yang sama

### Skilled (3 pts)
- [x] Monitoring Grafana dengan minimal 5 metriks berbeda
- [x] Membuat satu alerting menggunakan Grafana

## 📸 Screenshot yang Diperlukan

1. **1.bukti_serving/** - Screenshot terminal saat menjalankan `mlflow models serve`
2. **4.bukti monitoring Prometheus/** - Screenshot query di Prometheus untuk setiap metric
3. **5.bukti monitoring Grafana/** - Screenshot dashboard Grafana dengan nama username Dicoding
4. **6.bukti alerting Grafana/** - Screenshot alert rules dan notifikasi

## 🔧 Troubleshooting

### Model tidak bisa di-load
- Pastikan MLflow tracking server berjalan
- Pastikan run_id benar
- Check model path dengan: `mlflow models list`

### Prometheus tidak bisa scrape metrics
- Pastikan prometheus_exporter.py berjalan
- Check http://127.0.0.1:8000/metrics bisa diakses
- Pastikan prometheus.yml path benar

### Grafana tidak menampilkan data
- Pastikan Prometheus data source sudah di-setup
- Check query di Prometheus berfungsi
- Pastikan time range di Grafana benar

## 📝 Catatan Penting

1. **Dashboard Name:** Pastikan nama dashboard Grafana berisi username Dicoding Anda
2. **Model URI:** Ganti `MLFLOW_MODEL_URI` dengan path model Anda yang sebenarnya
3. **Ports:** Pastikan port 5000 (MLflow), 5001 (inference), 5002 (MLflow serve), 8000 (metrics), 9090 (Prometheus), 3000 (Grafana) tidak conflict

## 👤 Author

**Dinda Maulidiyah**

